from fastapi import APIRouter, Depends, HTTPException
from models.player import *
from handler.profile import *
from authy import *

route = APIRouter()

@route.post('/register', response_model=AuthResponse, dependencies=[Depends(verify_api_key)])
async def register_player(data: RegisterRequest):
    result = await register_user(data.email, data.password, data.phone)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@route.post('/login', response_model=AuthResponse, dependencies=[Depends(verify_api_key)])
async def login(data: LoginRequest):
    player = await authenticate_user(data.email, data.password)
    if not player:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Logged in", "player_id": player["player_id"]}

@route.get('/player/{player_id}', response_model=ProfileResponse, dependencies=[Depends(verify_api_key)])
async def get_player_profile(player_id: int):
    profile = await fetch_player_profile(player_id)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile

@route.put('/player/{player_id}', dependencies=[Depends(verify_api_key)])
async def update_player_profile(player_id: int, data: UpdateProfileRequest):
    result = await update_profile(player_id, data.phone, data.email, data.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@route.get('/player/{player_id}/stats', response_model=StatsResponse, dependencies=[Depends(verify_api_key)])
async def get_player_statistics(player_id: int):
    stats = await fetch_player_stats(player_id)
    if "error" in stats:
        raise HTTPException(status_code=404, detail=stats["error"])
    return stats

@route.post('/submit', response_model=SubmitSudokuResponse, dependencies=[Depends(verify_api_key)])
async def submit_sudoku(data: SubmitSudokuRequest):
    result = await submit_sudoku_result(data.player_id, data.sudoku_id, data.solve_time)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@route.get('/{player_id}/sudoku', dependencies=[Depends(verify_api_key)])
async def get_player_sudoku(player_id: int):
    sudoku = await fetch_player_sudoku(player_id)
    if "error" in sudoku:
        raise HTTPException(status_code=404, detail=sudoku["error"])
    return sudoku