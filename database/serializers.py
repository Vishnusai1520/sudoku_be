from pydantic import BaseModel
from typing import Optional

class PlayerSerializer(BaseModel):
    id: int
    username: str
    email: Optional[str]
    phone: Optional[str]
    current_streak: int
    highest_streak: int

    class Config:
        orm_mode = True


class SudokuSerializer(BaseModel):
    id: int
    puzzle: str
    solution: str
    best_time: int
    difficulty: str
    best_player: Optional[int]

    class Config:
        orm_mode = True


class PlayerSudokuSerializer(BaseModel):
    id: int
    player_id: int
    sudoku_id: int
    solve_time: int
    best_time: int

    class Config:
        orm_mode = True