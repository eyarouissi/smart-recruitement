from starlette.routing import Mount, Router 
import uvicorn
from config import settings 
from database.database import *
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from starlette.responses import Response
import json
import sys
from routes.Recruiter import router as StudentRouter
from starlette.applications import Starlette
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}

app.include_router(StudentRouter, tags=["v1"], prefix="/v1")


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
