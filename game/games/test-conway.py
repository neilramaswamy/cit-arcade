import os
import time
import random
import numpy as np
import pygame

# Conway's Game of Life - Board Size Input

def get_board_dimensions():
    try:
        rows = int(input("Enter the number of rows for the board: "))
        cols = int(input("Enter the number of columns for the board: "))
        if rows <= 0 or cols <= 0:
            print("Dimensions must be positive integers. Please try again.")
            return get_board_dimensions()
        return rows, cols
    except ValueError:
        print("Invalid input. Please enter positive integers.")
        return get_board_dimensions()

def create_initial_board(rows, cols):
    return np.random.randint(0,2,size=(rows, cols), dtype=int)

def display_board(board, cell_size):
    # os.system('cls' if os.name == 'nt' else 'clear')
    # for row in board:
    #     print(" ".join("█" if cell else " " for cell in row))
    rows, cols = board.shape
    for r in range(rows):
        for c in range(cols):
            color = (0, 0, 0) if board[r][c] == 0 else (255, 255, 255)
            pygame.draw.rect(screen, color, (c * cell_size, r * cell_size, cell_size, cell_size))
    pygame.display.flip()

def get_next_generation(board: np.ndarray) -> np.ndarray:
    rows, cols = board.shape
    next_board = np.zeros((rows, cols), dtype=int)
    start = time.time()
    for r in range(rows):
        for c in range(cols):
            live_neighbors = sum(
                board[nr][nc]
                for nr in range(max(0, r-1), min(rows, r+2))
                for nc in range(max(0, c-1), min(cols, c+2))
                if (nr, nc) != (r, c)
            )
            if board[r][c] == 1 and live_neighbors in (2, 3):
                next_board[r][c] = 1
            elif board[r][c] == 0 and live_neighbors == 3:
                next_board[r][c] = 1
    print(f'Took {time.time() - start}')
    return next_board

if __name__ == "__main__":
    rows, cols = 40,36
    board = create_initial_board(rows, cols)
    pygame.init()
    cell_size = 10
    screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
    pygame.display.set_caption("Conway's Game of Life")
    while True:
        display_board(board, cell_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        time.sleep(0.25)
        board = get_next_generation(board)