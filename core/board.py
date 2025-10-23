class Cell:
  """
  Represents a single cell in a Sudoku board.

  Attributes:
    x (int): The row index of the cell.
    y (int): The column index of the cell.
    collapsed (bool): True if the cell has a determined value, False otherwise.
    possible_values (list[int]): List of possible values for the cell. If collapsed, contains only the determined value.
  """

  def __init__(self, x: int, y: int, value: int) -> None:
    self.x: int = x
    self.y: int = y
    self.collapsed: bool
    self.possible_values: list[int]
    if value != 0:
      self.collapsed = True
      self.possible_values= [value]
    else:
      self.collapsed = False
      self.possible_values= list(range(1, 10))

  def __ne__(self, value: object) -> bool:
    """
    Determines whether two Cell objects are not equal based on position, collapse status, and possible values.

    Args:
      value (object): The other object to compare with.

    Returns:
      bool: True if the cells are not equal, False otherwise.
    """
    if not isinstance(value, Cell): return False
    return (self.x, self.y, self.collapsed, self.possible_values) != (value.x, value.y, value.collapsed, value.possible_values)


class Board:
  """
  Represents a 9x9 Sudoku board composed of Cell objects.

  Attributes:
    cells (list[list[Cell]]): 2D list representing the board's cells.
  """

  def __init__(self, cells: list[list[int]]) -> None:
    self.cells: list[list[Cell]] = []
    for x in range(len(cells)):
      row: list[Cell] = []
      for y in range(len(cells[0])):
        row.append(Cell(x, y, cells[x][y]))
      self.cells.append(row)

  def is_solved(self) -> bool:
    """
    Checks if the Sudoku board is completely solved.

    Returns:
      bool: True if all cells are collapsed, False otherwise.
    """
    for row in self.cells:
      for cell in row:
        if not cell.collapsed:
          return False
    return True

  def transpose(self) -> None:
    """
    Transposes the Sudoku board in-place, switching rows and columns.
    Updates cell coordinates accordingly.
    """
    self.cells = [list(row) for row in zip(*self.cells)]
    for x, row in enumerate(self.cells):
        for y, cell in enumerate(row):
            cell.x = x
            cell.y = y

  def find_cells_with_less_entropy(self) -> list[Cell]:
    """
    Finds the uncollapsed cells with the fewest possible values (least entropy).

    Returns:
      list[Cell]: List of cells with the minimum number of possible values.
    """
    flat_cells = [cell for row in self.cells for cell in row if not cell.collapsed]
    if not flat_cells:
      return []
    min_entropy_cells: list[Cell] = [flat_cells[0]]
    for i in range(1, len(flat_cells)):
      if len(flat_cells[i].possible_values) < len(min_entropy_cells[0].possible_values):
        min_entropy_cells = [flat_cells[i]]
      elif len(flat_cells[i].possible_values) == len(min_entropy_cells[0].possible_values):
        min_entropy_cells.append(flat_cells[i])
    return min_entropy_cells

  def print_board(self) -> None:
    """
    Prints a visual representation of the Sudoku board, showing possible values for uncollapsed cells.
    """
    def render_cell(cell: Cell) -> list[str]:
      grid = [[" " for _ in range(3)] for _ in range(3)]
      if cell.collapsed:
        grid[1][1] = str(cell.possible_values[0])
      else:
        for val in cell.possible_values:
          i = (val - 1) // 3
          j = (val - 1) % 3
          grid[i][j] = str(val)
      return ["".join(row) for row in grid]

    buffer: str = ""

    horizontal_block_line = "=" * ((3 + 1) * 9 + 4)

    buffer += f"{horizontal_block_line}\n"
    for row_idx, row in enumerate(self.cells):
      cell_lines = ["" for _ in range(3)]
      for col_idx, cell in enumerate(row):
        rendered = render_cell(cell)
        for i in range(3):
          cell_lines[i] += rendered[i]
          if (col_idx + 1) % 3 == 0 and col_idx != 8:
            cell_lines[i] += "||"
          else:
            cell_lines[i] += "|"
      for line in cell_lines:
        buffer += "|" + line + "\n"
      if (row_idx + 1) % 3 == 0 and row_idx != 8:
        buffer += f"{horizontal_block_line}\n"
    buffer += f"{horizontal_block_line}\n"
    print(buffer)

  def __eq__(self, value: object) -> bool:
    """
    Checks if two Sudoku boards are equal based on all cell states.

    Args:
      value (object): The other board to compare with.

    Returns:
      bool: True if boards are equal, False otherwise.
    """
    if not isinstance(value, Board): return False
    for x, row in enumerate(self.cells):
      for y, cell in enumerate(row):
        if cell != value.cells[x][y]:
          return False
    return True

  def is_invalid(self) -> bool:
    """
    Checks if the current board state violates Sudoku rules.

    Returns:
      bool: True if there are duplicate values in any row, column, or 3x3 square, False otherwise.
    """
    size = len(self.cells)
    for row in self.cells:
      values = [cell.possible_values[0] for cell in row if cell.collapsed]
      if len(values) != len(set(values)):
        return True
    for col in range(size):
      values = [
        self.cells[row][col].possible_values[0]
        for row in range(size)
        if self.cells[row][col].collapsed
      ]
      if len(values) != len(set(values)):
        return True
    square_size = int(size ** 0.5)
    for sx in range(square_size):
      for sy in range(square_size):
        values = []
        for x in range(sx * square_size, (sx + 1) * square_size):
          for y in range(sy * square_size, (sy + 1) * square_size):
            cell = self.cells[x][y]
            if cell.collapsed:
              values.append(cell.possible_values[0])
        if len(values) != len(set(values)):
          return True
    return False