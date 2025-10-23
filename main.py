import json
import time
from multiprocessing import Pool
from core.board import Board
from core.solver import solve

def solve_one(args):
  i, sudoku = args
  start = time.time()
  board = Board(sudoku['value'])
  ok = solve(board)
  end = time.time()
  return (i, board if ok else None, end - start)

if __name__ == "__main__":
  with open("./assets/sudokus.json", "r") as f:
    all_sudokus = json.load(f)

  waiting_results = {}
  next_to_print = 0

  with Pool() as pool:
    for i, board, duration in pool.imap_unordered(solve_one, list(enumerate(all_sudokus))):
      waiting_results[i] = (board, duration)
      while next_to_print in waiting_results:
        board, duration = waiting_results.pop(next_to_print)
        if board is None:
          print(f"COULD NOT SOLVE SUDOKU {next_to_print + 1}")
        else:
          print(f"SUDOKU {next_to_print + 1} SOLVED IN {duration:.4f}s")
          board.print_board()
        next_to_print += 1
