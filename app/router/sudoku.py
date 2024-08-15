from fastapi import APIRouter

from handler.sudoku import * 

route = APIRouter()

# @route.post('/login')

@route.get('/sudoku')
async def get_sudoku(difficulty:str):
    return await generate_puzzle(difficulty)

@route.post('/solve')
async def solve_sudoku(puzzle:dict):
    return await sudoku_solution(puzzle['grid'])