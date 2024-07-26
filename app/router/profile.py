from fastapi import APIRouter

from handler.profile import * 
from handler.sudoku import *

route = APIRouter()

@route.post('/login')
async def login():
    return {'message':'Logged in'}