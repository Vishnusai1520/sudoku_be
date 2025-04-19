import random
import copy
import sqlite3
import asyncio

conn = sqlite3.connect('sudoku.db')
cursor = conn.cursor()

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
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

def print_grid(grid):
    try:
        count = 0
        for row in grid:
            if count % 3 == 0:
                print('--------------------')
            count1 = 0
            for num in row:
                if count1 % 3 == 0:
                    print('|', end="")
                if num != 0:
                    print(num, end=" ")
                else:
                    print(". ", end="")
                count1 += 1
            print("")
            count += 1
        print('--------------------')
    except Exception as e:
        print(f"Error printing grid: {e}")

def is_valid(grid, num, row, col):
    try:
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False
        
        return True
    except Exception as e:
        print(f"Error in is_valid: {e}")
        return False

async def solve(grid):
    try:
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(grid, num, row, col):
                            grid[row][col] = num
                            if await solve(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True
    except Exception as e:
        print(f"Error solving Sudoku: {e}")
        return False

def divide_holes_into_nine(num_holes):
    try:
        holes = [min(num_holes // 9, 8)] * 9
        remaining_holes = num_holes - sum(holes)
        for i in range(remaining_holes):
            if holes[i] < 8:
                holes[i] += 1
        random.shuffle(holes)
        return holes
    except Exception as e:
        print(f"Error in divide_holes_into_nine: {e}")
        return []

def decode_puzzle(puzzle_str):
    return [[int(num) if num != '.' else 0 for num in puzzle_str[i:i+9]] for i in range(0, 81, 9)]

# def decode_solution(solution_str):
#     return [[int(num) for num in solution_str[i:i+9]] for i in range(0, 81, 9)]

async def generate_grid():
    try:
        grid = [[0 for _ in range(9)] for _ in range(9)]

        for k in range(0, 9, 3):
            numbers = random.sample(range(1, 10), 9)
            for i in range(3):
                for j in range(3):
                    grid[k+i][k+j] = numbers.pop()

        if not await solve(grid):
            print("Failed to solve the grid initially.")
            return None

        return grid
    except Exception as e:
        print(f"Error generating grid: {e}")
        return None
    
async def generate_puzzle_grid(grid,num_holes):
    try:
        holes = divide_holes_into_nine(num_holes)
        total_blanks = num_holes
        while total_blanks > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if grid[row][col] != 0 and holes[grid[row][col]-1]:
                grid[row][col] = 0
                holes[grid[row][col]-1] -= 1
                total_blanks -= 1
        return grid
    except Exception as e:
        print(f"Error generating solution: {e}")
        return None

async def get_holes(difficulty):
    num_holes = random.randint(58, 61)
    if difficulty == 'expert':
        num_holes = random.randint(49, 57)
    if difficulty == 'medium':
        num_holes = random.randint(40, 48)
    if difficulty == 'easy':
        num_holes = random.randint(30, 39)
    return num_holes

async def generate_puzzle(player_id, difficulty):
    try:
        cursor.execute('''SELECT ps.sudoku_id, s.puzzle, s.solution FROM player_sudoku ps 
                  JOIN sudoku s ON ps.sudoku_id = s.id 
                  WHERE ps.player_id=? AND s.difficulty=? and solve_time = 0''', (player_id, difficulty))
        
        existing_puzzle = cursor.fetchone()
        
        print(f"Existing puzzle for player {player_id} with difficulty {difficulty}: {existing_puzzle}")
        if existing_puzzle:
            print(f"Player {player_id} already has an assigned Sudoku with difficulty {difficulty}.")
            grid = decode_puzzle(existing_puzzle[1])
            solution = decode_puzzle(existing_puzzle[2])
            return {'sudoku_id' :existing_puzzle[0] ,'puzzle': grid, 'solution': solution}

        grid = await generate_grid()

        solution = copy.deepcopy(grid)
        num_holes = await get_holes(difficulty)

        puzzle = await generate_puzzle_grid(grid, num_holes)

        puzzle_str = ''.join([''.join([str(num) if num != 0 else '.' for num in row]) for row in puzzle])
        solution_str = ''.join([''.join([str(num) for num in row]) for row in solution])

        cursor.execute('''INSERT INTO sudoku (puzzle, solution, difficulty) VALUES (?, ?, ?)''',
                       (puzzle_str, solution_str, difficulty))
        sudoku_id = cursor.lastrowid
        conn.commit()

        cursor.execute('''INSERT INTO player_sudoku (player_id, sudoku_id) VALUES (?, ?)''',
                       (player_id, sudoku_id))
        conn.commit()

        print("Puzzle:")
        print_grid(grid)
        print("Solution:")
        print_grid(solution)

        return {'sudoku_id': sudoku_id,'puzzle': grid, 'solution': solution}
    except Exception as e:
        print(f"Error generating puzzle: {e}")
        return None

async def sudoku_solution(grid):
    try:
        print("Puzzle:")
        print_grid(grid)
        for i in range(9):
            for j in range(9):
                if grid[i][j] == '':
                    grid[i][j] = 0

        if not await solve(grid):
            print("Failed to solve the grid initially.")
            return None

        print("Solution:")
        print_grid(grid)

        return {'solution': grid}
    except Exception as e:
        print(f"Error solving Sudoku: {e}")
        return None
