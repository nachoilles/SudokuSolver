import json
from board import Board, Cell
import copy



def collapse(board: Board) -> Board:
  board = collapse_by_row(board)
  board = collapse_by_column(board)
  board = collapse_squares(board, 3)
  return board

def collapse_squares(board: Board, square_size: int) -> Board:
  if len(board.cells) % square_size != 0 or len(board.cells[0]) % square_size != 0:
    raise ValueError(f"[Value Error]: square_size ({square_size}) is not a divisor of one or both of the dimensions of the board ({len(board.cells)} x {len(board.cells[0])})")

  for square_x in range(len(board.cells) // square_size):
    for square_y in range(len(board.cells[0]) // square_size):
      square_cells = [cell for row in board.cells for cell in row
                if square_x * square_size <= cell.x < (square_x+1) * square_size
                and square_y * square_size <= cell.y < (square_y+1) * square_size]
      collapsed_values = [cell.possible_values[0] for cell in square_cells if cell.collapsed]
      collapsed_cells = collapse_list(square_cells, collapsed_values)
      for cell in collapsed_cells:
        board.cells[cell.x][cell.y] = cell

  return board

def collapse_by_column(board: Board) -> Board:
  board.transpose()
  board = collapse_by_row(board)
  board.transpose()
  return board

def collapse_by_row(board: Board) -> Board:
  for x, row in enumerate(board.cells):
    collapsed_values = []
    for cell in row:
      if cell.collapsed:
        collapsed_values.append(cell.possible_values[0])

    board.cells[x] = collapse_list(row, collapsed_values)
  return board

def collapse_list(cell_list: list[Cell], collapsed_values: list[int]) -> list[Cell]:
  new_cell_list: list[Cell] = []
  for cell in cell_list:
    if not cell.collapsed:
      cell.possible_values = [value for value in cell.possible_values if value not in collapsed_values]
      if len(cell.possible_values) == 1:
        cell.collapsed = True
      new_cell_list.append(cell)
    else:
      new_cell_list.append(cell)
  return new_cell_list

if __name__ == "__main__":
  with open("../assets/sudokus.json", "r") as f:
    all_sudokus = json.load(f)
    board: Board = Board(all_sudokus[0]['value'])
    board.print_board()
    for _ in range(2):
      previous_board: Board = copy.deepcopy(board)
      collapse(board)
      board.print_board()
      if previous_board == board:
        print("NO IMPROVEMENT")
      else:
        print("SUCCESFULLY COLLAPSED")