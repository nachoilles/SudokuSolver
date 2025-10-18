class Cell:
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

  def __eq__(self, value: object) -> bool:
    if not isinstance(value, Cell): return False
    return self.x == value.x and self.y == value.y and self.collapsed == value.collapsed and self.possible_values == value.possible_values

  def __ne__(self, value: object) -> bool:
    if not isinstance(value, Cell): return False
    return self.x != value.x or self.y != value.y or self.collapsed != value.collapsed or self.possible_values != value.possible_values


class Board:
  def __init__(self, cells: list[list[int]]) -> None:
    self.cells: list[list[Cell]] = []
    for x in range(len(cells)):
      row: list[Cell] = []
      for y in range(len(cells[0])):
        row.append(Cell(x, y, cells[x][y]))
      self.cells.append(row)

  def is_solved(self) -> bool:
    for row in self.cells:
      for cell in row:
        if not cell.collapsed:
          return False
    return True

  def transpose(self) -> None:
    self.cells = [list(row) for row in zip(*self.cells)]
    for x, row in enumerate(self.cells):
        for y, cell in enumerate(row):
            cell.x = x
            cell.y = y

  def print_board(self) -> None:
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

    horizontal_block_line = "=" * (9 * (3 * 3 + 2) + 10)
    subblock_line = "-" * (9 * (3 * 3 + 2) + 10)

    print(horizontal_block_line)
    for row_idx, row in enumerate(self.cells):
      cell_lines = ["" for _ in range(3)]
      for col_idx, cell in enumerate(row):
        rendered = render_cell(cell)
        for i in range(3):
          cell_lines[i] += " " + rendered[i] + " "
          if (col_idx + 1) % 3 == 0 and col_idx != 8:
            cell_lines[i] += " || "
          else:
            cell_lines[i] += "|"
      for line in cell_lines:
        print("|" + line)
      if (row_idx + 1) % 3 == 0 and row_idx != 8:
        print(subblock_line)
    print(horizontal_block_line)


  def __eq__(self, value: object) -> bool:
    if not isinstance(value, Board): return False
    for x, row in enumerate(self.cells):
      for y, cell in enumerate(row):
        if cell != value.cells[x][y]:
          return False
    return True