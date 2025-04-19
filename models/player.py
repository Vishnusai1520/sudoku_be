from pydantic import BaseModel
from typing import Optional, Dict


class RegisterRequest(BaseModel):
    email:str
    password: str
    phone: Optional[str] = None

class LoginRequest(BaseModel):
    email:str
    password: str

class UpdateProfileRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class AuthResponse(BaseModel):
    message: str
    player_id: int

class ProfileResponse(BaseModel):
    player_id: int
    email: str
    phone: Optional[str]
    current_streak: int
    highest_streak: int

class StatsResponse(BaseModel):
    current_streak: int
    highest_streak: int
    best_times: Dict[str, Optional[int]]  

class SubmitSudokuRequest(BaseModel):
    player_id: int
    sudoku_id: int
    solve_time: int 

class SubmitSudokuResponse(BaseModel):
    updated_time: int
    current_streak: int
    highest_streak: int
