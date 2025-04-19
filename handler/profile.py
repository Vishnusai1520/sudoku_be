import sqlite3
from database.db import SessionLocal
from database.models import Player
from database.serializers import PlayerSerializer

conn = sqlite3.connect('sudoku.db')
cursor = conn.cursor()
db = SessionLocal()

def create_tables():
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS sudoku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            puzzle TEXT NOT NULL,
            solution TEXT NOT NULL,
            best_time INTEGER DEFAULT 0,
            best_player INTEGER,
            difficulty TEXT DEFAULT 'easy'
        );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            current_streak INTEGER DEFAULT 0,
            highest_streak INTEGER DEFAULT 0,
            password TEXT NOT NULL,
            phone TEXT,
            email TEXT
        );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS player_sudoku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            sudoku_id INTEGER NOT NULL,
            solve_time INTEGER DEFAULT 0,
            best_time INTEGER DEFAULT 0
        );''')
        
        conn.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")

create_tables()

def signupHandler(username:str, password:str, email:str, phone_number:str) -> tuple[bool, any]:
    print("entered handler")

    player_exists = db.query(Player).filter(Player.username == username).first()
    if player_exists:
        return (False, f"User with username:{username} already exists")
    
    player = Player(
        username=username,
        password=password,
        email=email,
        phone=phone_number
    )
    db.add(player)
    db.commit()
    db.refresh(player)
    player_data = model_to_dict(player)
    player_data.pop("password", None)
    db.close()

    return True, {"player": player_data, "error": None}

def loginHandler(username:str, password:str) -> tuple[bool, any]:
    player = db.query(Player).filter(Player.username == username).first()

    if not player:
        return False, {"error": f"No user with exists with username:{username}"}
    
    if player.password != password:
        return False, {"error": "Unauthorized"}
    
    player_data = model_to_dict(player)
    player_data.pop("password", None)
    db.close()

    return True, {"player": player_data, "error": None}


def model_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}