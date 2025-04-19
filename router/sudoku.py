from fastapi import APIRouter, Depends
from handler.sudoku import *
from authy import * 

route = APIRouter()

@route.get('/sudoku', dependencies=[Depends(verify_api_key)])
async def get_sudoku(player_id: int,difficulty:str):
    return await generate_puzzle(player_id,difficulty)

@route.post('/solve', dependencies=[Depends(verify_api_key)])
async def solve_sudoku(puzzle:dict):
    return await sudoku_solution(puzzle['grid'])
