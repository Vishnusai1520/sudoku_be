import random
import copy

def print_grid(grid):
    count = 0
    for row in grid:
        if count%3==0:
            print('--------------------')
        count1 = 0
        for num in row:
            if count1%3 ==0:
                print('|',end="")
            if num !=0 :
                print(num,end=" ")
            else:
                print(". ",end="")
            count1+=1
        print("")
        count+=1
    print('--------------------')
        
def is_valid(grid, num, row, col):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    
    return True

async def solve(grid):
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

def divide_holes_into_nine(num_holes):
    total_blanks = num_holes
    avg_holes = num_holes // 9
    holes = []
    nine_count = 0
    excess_hole = []
    for i in range(8):
        avg_hole = num_holes // (9 - i)
        if avg_hole > 9:
            excess_hole.append(avg_hole-9)
            avg_hole = 9
        else:
            excess_hole.append(0)

        blank = avg_hole

        if avg_hole != 9:
            if random.randint(1, 100) % 2:
                blank = random.randint(max(1, avg_hole), min(9, num_holes))
            else:
                blank = random.randint(1, min(avg_hole, 9))
        else:
            blank = 8
        if blank == 9:
            nine_count += 1
            if nine_count > 1:
                blank = 8 
        holes.append(blank)
        num_holes -= blank
    excess_hole.append(0)
    if num_holes == 9 and nine_count > 0:
        holes.append(8)
        num_holes -= 8
    elif num_holes < 9:
        holes.append(num_holes)
    else:
        excess = num_holes - 9
        holes.append(9)
        avg_exc = excess
        if excess > 2:
            avg_exc = excess//2
        for i in range(9):
            holes[i] += excess_hole[i]
            if holes[i] + avg_exc < 9 and excess>0:
                inc = min(avg_exc,excess)
                holes[i] += inc
                excess -= inc

    if holes.count(9) > 1:
        for i in range(9):
            if holes[i] >= 9:
                excess = holes[i] - 8
                holes[i] = 8
                for j in range(9):
                    increment = min(9 - holes[j], excess)
                    if holes[j] + increment < 9 and excess > 0:
                        holes[j] += increment
                        excess -= increment
                        if excess == 0:
                            break

    return holes

async def generate_puzzle(difficulty):
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    for k in range(0, 9, 3):
        numbers = random.sample(range(1, 10), 9)
        for i in range(3):
            for j in range(3):
                grid[k+i][k+j] = numbers.pop()
    # print_grid(grid)
    if not await solve(grid):
        print("Failed to solve the grid initially.")
        return None

    solution = copy.deepcopy(grid)
    num_holes = random.randint(58,61)
    if difficulty == 'expert':
        num_holes = random.randint(49, 57)
    if difficulty == 'medium':
        num_holes = random.randint(40,48)
    if difficulty == 'easy':
        num_holes = random.randint(30,39)
    
    holes = divide_holes_into_nine(num_holes)
    total_blanks = num_holes
    print(holes)
    while total_blanks > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0 and holes[grid[row][col]-1]:
            grid[row][col] = 0
            holes[grid[row][col]-1]-=1
            total_blanks-=1 

    print("Puzzle:")
    print_grid(grid)
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                grid[i][j] = ''
    response = {
        'puzzle': copy.deepcopy(grid),
        'solution': solution
    }
    print("Solution:")
    print_grid(response['solution'])
    return response

async def sudoku_solution(grid):
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
    
    return {'solution':grid}