from fastapi import APIRouter

from handler.sudoku import * 

route = APIRouter()

# @route.post('/login')

@route.get('/sudoku')
async def get_sudoku(difficulty:str,player_id : int):
    return await generate_puzzle(difficulty,player_id)

@route.post('/solve')
async def solve_sudoku(puzzle:dict):
    return await sudoku_solution(puzzle['grid'])