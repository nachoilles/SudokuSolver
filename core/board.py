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

  def find_cells_with_less_entropy(self) -> list[Cell]:
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

    horizontal_block_line = "=" * ((3 + 1) * 9 + 4)

    print(horizontal_block_line)
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
        print("|" + line)
      if (row_idx + 1) % 3 == 0 and row_idx != 8:
        print(horizontal_block_line)
    print(horizontal_block_line)

  def __eq__(self, value: object) -> bool:
    if not isinstance(value, Board): return False
    for x, row in enumerate(self.cells):
      for y, cell in enumerate(row):
        if cell != value.cells[x][y]:
          return False
    return True

  def is_invalid(self) -> bool:
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
