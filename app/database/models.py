from sqlalchemy import Column, Integer, String, ForeignKey
from .db import Base

class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True)
    phone = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    current_streak = Column(Integer, default = 0)
    highest_streak = Column(Integer, default = 0)

    
class Sudoku(Base):
    __tablename__ = "sudoku"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    puzzle = Column(String(255), nullable=False)
    solution = Column(String(255), nullable=False)
    best_time = Column(Integer, default = 0)
    difficulty = Column(String(255), default='easy')
    best_player = Column(Integer, ForeignKey('player.id'), default=None)


class PlayerSudoku(Base):
    __tablename__ = "player_sudoku"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    sudoku_id = Column(Integer, ForeignKey('sudoku.id'), nullable=False)
    solve_time = Column(Integer, default = 0)
    best_time = Column(Integer, default = 0) # is the best time needed here?
