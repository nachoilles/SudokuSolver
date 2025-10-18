from .board import Board, Cell
import copy

def collapse(board: Board) -> Board:
  """
  Repeatedly collapses the board by rows, columns, and squares until no further changes occur.

  Args:
    board (Board): The Sudoku board to collapse.

  Returns:
    Board: The collapsed board.
  """
  changed = True
  while changed:
    previous_board = copy.deepcopy(board)
    board = collapse_by_row(board)
    board = collapse_by_column(board)
    board = collapse_squares(board, 3)
    changed = previous_board != board
  return board

def collapse_squares(board: Board, square_size: int) -> Board:
  """
  Collapses the board by removing impossible values based on 3x3 square constraints.

  Args:
    board (Board): The Sudoku board to collapse.
    square_size (int): Size of the square blocks (typically 3 for 9x9 Sudoku).

  Returns:
    Board: The board after collapsing squares.

  Raises:
    ValueError: If square_size does not divide the board dimensions evenly.
  """
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
  """
  Collapses the board by removing impossible values based on column constraints.

  Args:
    board (Board): The Sudoku board to collapse.

  Returns:
    Board: The board after collapsing columns.
  """
  board.transpose()
  board = collapse_by_row(board)
  board.transpose()
  return board

def collapse_by_row(board: Board) -> Board:
  """
  Collapses the board by removing impossible values based on row constraints.

  Args:
    board (Board): The Sudoku board to collapse.

  Returns:
    Board: The board after collapsing rows.
  """
  for x, row in enumerate(board.cells):
    collapsed_values = []
    for cell in row:
      if cell.collapsed:
        collapsed_values.append(cell.possible_values[0])

    board.cells[x] = collapse_list(row, collapsed_values)
  return board

def collapse_list(cell_list: list[Cell], collapsed_values: list[int]) -> list[Cell]:
  """
  Removes collapsed values from the possible values of uncollapsed cells in a list.

  Args:
    cell_list (list[Cell]): List of cells to process.
    collapsed_values (list[int]): Values to remove from uncollapsed cells.

  Returns:
    list[Cell]: Updated list of cells after collapsing.
  """
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

def solve(board: Board) -> bool:
  """
  Attempts to solve the Sudoku board using constraint propagation and backtracking.

  Args:
    board (Board): The Sudoku board to solve.

  Returns:
    bool: True if the board is solved successfully, False if unsolvable.
  """
  collapse(board)

  if board.is_invalid():
    return False

  if board.is_solved():
    return True

  cells = board.find_cells_with_less_entropy()
  if not cells:
    return False

  cell = cells[0]

  for value in cell.possible_values:
    new_board = copy.deepcopy(board)
    new_board.cells[cell.x][cell.y].possible_values = [value]
    new_board.cells[cell.x][cell.y].collapsed = True
    if solve(new_board):
      board.cells = new_board.cells
      return True

  return False