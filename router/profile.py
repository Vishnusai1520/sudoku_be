from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from handler.profile import * 
from handler.sudoku import *
from authy import *

route = APIRouter()

#TODO: Need to add some type of hashing for password or use fastAPI security methods

class SignUpRequest(BaseModel):
    username: str
    password:str
    email:str
    phone:str


class LoginRequest(BaseModel):
    username: str
    password: str


@route.post('/login', dependencies=[Depends(verify_api_key)])
async def login():
    return {'message':'Logged in'}

@route.post('/signup', dependencies=[Depends(verify_api_key)])
def signup(request: SignUpRequest):
    username=request.username
    password=request.password
    email=request.email
    phone=request.phone

    is_successful, data = signupHandler(username, password, email, phone)
    if not is_successful:
        return JSONResponse(status_code=422, content={"message": data})
    return JSONResponse(status_code=201, content=data)

@route.post('/login_v2', dependencies=[Depends(verify_api_key)])
def login_v2(request: LoginRequest):
    username = request.username
    password = request.password
    is_successful, data = loginHandler(username, password)
    if not is_successful:
        return JSONResponse(status_code=401, content=data)
    return JSONResponse(status_code=200, content=data)