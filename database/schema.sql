CREATE TABLE sudoku (
    id INT PRIMARY KEY AUTO_INCREMENT,
    puzzle VARCHAR(255) NOT NULL,
    solution VARCHAR(255) NOT NULL,
    best_time INT DEFAULT 0,
    best_player INT,
    difficulty VARCHAR(255) DEFAULT 'easy'
);

CREATE TABLE player (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    current_streak INT DEFAULT 0,
    highest_streak INT DEFAULT 0,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE player_sudoku (
    id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT NOT NULL,
    sudoku_id INT NOT NULL,
    solve_time INT DEFAULT 0,
    best_time INT DEFAULT 0
);
