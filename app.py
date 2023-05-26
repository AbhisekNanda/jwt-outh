from typing import List
from fastapi import FastAPI,Form
from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import json
import jwt
import db

import database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()


class login(BaseModel):
    email : str
    password : str

@app.post("/token")
def get_token(form_data : OAuth2PasswordRequestForm = Depends()):
    
    my_secret = 'my_super_secret'
    #payload_data = database.login()
    payload_data=db.login(form_data.username,form_data.password)
    
    
    token = jwt.encode(
    payload=payload_data,
    key=my_secret
    )
    
    return token

@app.get("/data")
def database(token:str = Depends(oauth2_scheme)):
    return "data"

@app.get("/")
def index():
    return "index"

class User(BaseModel):
    First_name : str
    Second_name : str
    email : str
    password : str


@app.post('/signup')
def signup(user:User):
    if db.check_email(user.email):
        return "User already exist"
    else:
        status=db.create_user(user.id,user.First_name,user.Second_name,user.email,user.password)
        return status