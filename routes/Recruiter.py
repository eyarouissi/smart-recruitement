#from _typeshed import ReadableBuffer
from re import MULTILINE
import pydantic
from bson import ObjectId
import bson
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str
from fastapi import APIRouter, Body,  Request
from fastapi.encoders import jsonable_encoder
import pymongo
from starlette.routing import request_response 
from database.database import *
from models.Employee import *
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
import  pymongo
import asyncio
router = APIRouter()


#Returns the roles
@router.get("/roles", response_description="roles retrieved")
async def get_roles():

    doc = list ( Roles_collection.find())
    
    if doc == [] :
     return ErrorResponseModel("An error occured.", 404, " The roles are not found")
    else :
     
     
     return ResponseModel_get(doc, "Roles retrieved successfully")
    
#Returns competencies 
@router.get("/competencies", response_description="competencies retrieved")
async def competencies():

    doc = list ( Competencies_collection.find({}))
    
    if doc == [] :
     return ErrorResponseModel("An error occured.", 404, " The competencies are not found")
    else :
     
     
     return ResponseModel_get(doc, "Competencies retrieved successfully")
    
#Returns the competencies by role
@router.get("/competencies-by-role", response_description="competencies retrieved")
async def competencies_by_role(role_name:str):
    if role_name=="":
          return ErrorResponseModel("An error occured.", 404, " The role id is not valid")
    else :
     doc = list ( Roles_collection.find({"roleName": role_name}))
     if doc==[]:
          return ErrorResponseModel("An error occured.", 404, " The role name is not found")
     else :
      competencies_list =[]
      competency=[]
      role =  doc[0]
      top_competencies = role["roleCompetencies"]

      for i in range(len(top_competencies)) :
       competency = list ( Competencies_collection.find({"_id": ObjectId(top_competencies[i])}))
       competencies_list.append(competency[0])
       competency=[] 

    
      return ResponseModel_get(competencies_list, "Competencies retrieved successfully")




@router.post("/register-recruiter", response_description="user registered as a manager in our DB")
async def register_recruiter(request: Request):
    user_data = await request.json()
    #user_data = jsonable_encoder(request)
    user_email=user_data['email']
    user_password=user_data['password']
    user_firstName=user_data['firstName']
    user_middleName=user_data['middleName']
    user_lastName=user_data['lastName']
    user_phone=user_data['phone']
    user_id=ObjectId()
    manager_id=ObjectId()
    Users_collection.insert_one({ "_id":user_id,"userFirstName":user_firstName,"userMiddleName":user_middleName,"userLastName":user_lastName,"userPhone":user_phone,"userEmail": user_email,"userPassword":user_password})
    Recruiters_collection.insert_one({"_id":manager_id,"managerUserId":user_id,"managerProjectIds":[]})
      
    return ResponseModel_post("", "the user is successfully registered as a manager in our DB")
      
#Checks if the email and password correspond to an existing reruiter.
@router.post("/login-recruiter", response_description="manager exists in our DB")
async def login_recruiter(request: Request):
    user_data = await request.json()
    user_email=user_data['useremail']
    user_password=user_data['password']

    doc_id = list ( Users_collection.find({ "userEmail": user_email,"userPassword":user_password}))

    if doc_id == []  :
             return ErrorResponseModel("user not found in our DB", 404, "Please make sure you entered the right email and password")
    else:
      user_id=doc_id[0]['_id']
      doc_recruiter = list ( Recruiters_collection.find({ "recruiterUserId": user_id}))
      if doc_recruiter==[]:
          return ErrorResponseModel("user not registered as recruiter ", 404, " The email of this employee is not found in recruiters collection") 
    
      return ResponseModel_post("", "the email and password correspond to an existing manager.")

#Returns the list of the projects a manager has.
@router.get("/recruiter-projects", response_description="projects retrieved")
async def projects(user_email:str):
    doc_user=list ( Users_collection.find({ "userEmail": user_email}))
    user_id=doc_user[0]['_id']
    doc = list ( Recruiters_collection.find({"recruiterUserId":user_id}))
    
    if doc == [] :
     return ErrorResponseModel("An error occured.", 404, " This user is not registered as manager ")
    else :
        data=[]
        projects=doc[0]['recruiterProjectId']
        for project in projects:
            doc_project = list ( Projects_collection.find({ "_id": project}))
            data.append(doc_project[0])
            
            
     
     
        return ResponseModel_get(data, "Projects retrieved successfully")
