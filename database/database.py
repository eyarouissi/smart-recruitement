from pymongo.mongo_client import MongoClient
import motor.motor_asyncio
from bson import ObjectId
from pydantic.networks import EmailStr
import ssl
import pymongo 
from models import  * 
import os
from dotenv import load_dotenv

load_dotenv()
mongo_details = os.getenv('MONGO_DETAILS')
client = pymongo.MongoClient(mongo_details, ssl=True)
database = client['smart-recruitement']

Roles_collection = database.get_collection('roles')
Competencies_collection = database.get_collection('competencies')
Questions_collection = database.get_collection('Questions')
Employees_collection = database.get_collection('employees')
TailoredRole_collection = database.get_collection('TailoredRole')
Users_collection = database.get_collection('users')
Managers_collection = database.get_collection('managers')
Projects_collection = database.get_collection('projects')
Recruiters_collection = database.get_collection('recruiters')







   
   









