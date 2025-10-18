import json
from core.board import Board
from core.solver import solve

if __name__ == "__main__":
  with open("./assets/sudokus.json", "r") as f:
    all_sudokus = json.load(f)
    for i, sudoku in enumerate(all_sudokus):
      board: Board = Board(sudoku['value'])
      solution: Board = Board(sudoku['solution'])
      if solve(board):
        print(f"SUDOKU {i + 1} SOLVED")
        board.print_board()
      else:
        print(f"COULD NOT SOLVE SUDOKU {i + 1}")