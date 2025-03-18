from fastapi import APIRouter

from handler.profile import * 
from handler.sudoku import *
from authy import *

route = APIRouter()

@route.post('/login', dependencies=[Depends(verify_api_key)])
async def login():
    return {'message':'Logged in'}