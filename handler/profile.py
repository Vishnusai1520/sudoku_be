import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db_connection():
    return sqlite3.connect('sudoku.db', check_same_thread=False)

async def register_user(email: str, password: str, phone: str = None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT player_id FROM player WHERE email=?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return {"error": "Email already registered"}

        hashed_password = pwd_context.hash(password)

        cursor.execute(
            "INSERT INTO player (email, password, phone) VALUES (?, ?, ?)",
            (email, hashed_password, phone)
        )
        conn.commit()
        player_id = cursor.lastrowid
        conn.close()

        return {"message": "Player registered successfully", "player_id": player_id}
    except Exception as e:
        return {"error": f"Error registering player: {e}"}

async def authenticate_user(email: str, password: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT player_id, password FROM player WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and pwd_context.verify(password, user[1]):
            return {"player_id": user[0]}
        return None
    except Exception as e:
        return {"error": f"Error during authentication: {e}"}

async def fetch_player_profile(player_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT player_id, email, phone, current_streak, highest_streak FROM player WHERE player_id=?",
            (player_id,)
        )
        user = cursor.fetchone()
        conn.close()

        if not user:
            return {"error": "Player not found"}

        return {
            "player_id": user[0],
            "email": user[1],
            "phone": user[2],
            "current_streak": user[3],
            "highest_streak": user[4]
        }
    except Exception as e:
        return {"error": f"Error fetching player profile: {e}"}

async def update_profile(player_id: int, phone: str = None, email: str = None, password: str = None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        update_fields = []
        params = []

        if email:
            update_fields.append("email=?")
            params.append(email)

        if phone:
            update_fields.append("phone=?")
            params.append(phone)

        if password:
            hashed_password = pwd_context.hash(password)
            update_fields.append("password=?")
            params.append(hashed_password)

        if not update_fields:
            return {"error": "No fields to update"}

        query = f"UPDATE player SET {', '.join(update_fields)} WHERE player_id=?"
        params.append(player_id)

        cursor.execute(query, tuple(params))
        conn.commit()
        conn.close()

        return {"message": "Profile updated successfully"}
    except Exception as e:
        return {"error": f"Error updating profile: {e}"}

async def fetch_player_stats(player_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT current_streak, highest_streak FROM player WHERE player_id=?",
            (player_id,)
        )
        streaks = cursor.fetchone()
        if not streaks:
            return {"error": "Player not found"}

        
        cursor.execute("""
            SELECT s.difficulty, MIN(ps.best_time)
            FROM player_sudoku ps
            JOIN sudoku s ON ps.sudoku_id = s.id
            WHERE ps.player_id=? AND ps.best_time > 0
            GROUP BY s.difficulty
        """, (player_id,))
        rows = cursor.fetchall()

        best_times = {"easy": None, "medium": None, "expert": None}
        for diff, time in rows:
            best_times[diff] = time

        conn.close()
        return {
            "current_streak": streaks[0],
            "highest_streak": streaks[1],
            "best_times": best_times
        }
    except Exception as e:
        return {"error": f"Error fetching player stats: {e}"}


async def update_streak(player_id: int, streak_type: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if streak_type == "current":
            cursor.execute("UPDATE player SET current_streak = current_streak + 1 WHERE player_id=?", (player_id,))
        elif streak_type == "highest":
            cursor.execute(
                "UPDATE player SET highest_streak = CASE WHEN current_streak > highest_streak THEN current_streak ELSE highest_streak END WHERE player_id=?",
                (player_id,)
            )
        else:
            return {"error": "Invalid streak type"}

        conn.commit()
        conn.close()

        return {"message": f"{streak_type.capitalize()} streak updated"}
    except Exception as e:
        return {"error": f"Error updating streak: {e}"}

async def submit_sudoku_result(player_id: int, sudoku_id: int, solve_time: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE player_sudoku SET solve_time = ? WHERE player_id=? AND sudoku_id=?",
            (solve_time, player_id, sudoku_id)
        )
        cursor.execute(
            "UPDATE player SET current_streak = current_streak + 1 WHERE player_id=?",
            (player_id,)
        )
        cursor.execute(
            "UPDATE player SET highest_streak = CASE WHEN current_streak > highest_streak THEN current_streak ELSE highest_streak END WHERE player_id=?",
            (player_id,)
        )
        cursor.execute(
            "UPDATE player_sudoku SET best_time = CASE WHEN best_time IS NULL OR ? < best_time THEN ? END WHERE player_id=? AND sudoku_id=?",
            (solve_time, solve_time, player_id, sudoku_id)
        )
        conn.commit()
        cursor.execute(
            "SELECT current_streak, highest_streak FROM player WHERE player_id=?",
            (player_id,)
        )
        streaks = cursor.fetchone()
        
        conn.close()
        if not streaks:
            return {"error": "Player not found"}
        return {
            "updated_time": solve_time,
            "current_streak": streaks[0],
            "highest_streak": streaks[1]
        }
    except Exception as e:
        return {"error": f"Error submitting Sudoku result: {e}"}

async def fetch_player_sudoku(player_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ps.sudoku_id, s.puzzle, s.solution, ps.solve_time
            FROM player_sudoku ps
            JOIN sudoku s ON ps.sudoku_id = s.id
            WHERE ps.player_id=?
        """, (player_id,))
        sudoku_data = cursor.fetchall()

        if not sudoku_data:
            return {"error": "No Sudoku puzzles found for this player"}

        puzzles = [
            {
                "sudoku_id": row[0],
                "puzzle": row[1],
                "solution": row[2],
                "solve_time": row[3]
            }
            for row in sudoku_data
        ]

        conn.close()
        return puzzles
    except Exception as e:
        return {"error": f"Error fetching player Sudoku: {e}"}
