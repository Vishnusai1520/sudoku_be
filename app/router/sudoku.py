from fastapi import APIRouter
from fastapi import Depends

from handler.sudoku import * 
from authy import *

route = APIRouter()

# @route.post('/login')

@route.get('/sudoku', dependencies=[Depends(verify_api_key)])
async def get_sudoku(difficulty:str):
    return await generate_puzzle(difficulty)

@route.post('/solve', dependencies=[Depends(verify_api_key)])
async def solve_sudoku(puzzle:dict):
    return await sudoku_solution(puzzle['grid'])