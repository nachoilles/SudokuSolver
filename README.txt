SudokuSolver
============

Description:
-------------
SudokuSolver is a Python application that solves Sudoku puzzles using a constraint-propagation
and backtracking algorithm. It supports solving multiple puzzles from a JSON file and prints
the solution in a clear, visual format.

Setup Instructions:
-------------------
1. Python Environment Setup:
   - Open a terminal or PowerShell in the project root.
   - Run the environment setup script to create a virtual environment and install dependencies:
       scripts\setup-env.bat

2. Download Sudoku Puzzles:
   - To download or update the Sudoku puzzles, run the following script:
       python scripts\get-sudokus.py
   - This will populate the ./assets/sudokus.json file with puzzles.

Usage:
------
1. Run the main script to solve all Sudoku puzzles listed in ./assets/sudokus.json:
       python main.py

2. For each puzzle, the program will:
   - Attempt to solve the Sudoku using constraint propagation and backtracking.
   - Print the solved board if successful.
   - Indicate if a puzzle could not be solved.

File Structure:
---------------
SudokuSolver/
├─ core/
│  ├─ __init__.py
│  ├─ board.py                    # Contains Board and Cell classes for Sudoku representation
│  ├─ solver.py                   # Contains the solver logic
├─ scripts/
│  ├─ setup-env.bat               # Script to create Python environment and install dependencies
│  ├─ get-sudokus.py              # Script to download Sudoku puzzles
│  ├─ install-dependencies.bat    # Script to install dependencies (called by setup-env.bat)
├─ assets/
│  ├─ sudokus.json                # Sudoku puzzles in JSON format (once downloaded through get-sudokus.py)
├─ main.py                        # Entry point for solving Sudokus