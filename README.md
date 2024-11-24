# Solving Sokoban using Formal Verification
Welcome to the Sokoban Solver Project!
This repository contains models and scripts designed to solve Sokoban puzzles using formal verification methods and automated testing.
The project focuses on modeling Sokoban boards and optimizing performance through advanced algorithms and techniques.


---

## Table of Contents
- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Features](#features)
- [Usage](#usage)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---
## Overview

Sokoban is a classic puzzle game where the goal is to push boxes onto designated goal locations within a grid-like board. 
The player can only push one box at a time and must plan movements carefully to avoid deadlocks and achieve the solution.

This project provides a framework for solving Sokoban puzzles by modeling the boards as Fair Discrete Systems (FDS) and leveraging the formal verification tool NuXmv to check solvability. Additionally, the project includes an automation script capable of running multiple solvers on multiple Sokoban boards, making it highly extensible for testing and benchmarking purposes.


### Key Features:

1. **Input Format**:
   - Sokoban boards are provided in **XSB format**, specifying the layout of walls, boxes, the player, and goal positions.

2. **Modeling as FDS**:
   - Each board is modeled as a **Fair Discrete System** using the **SMV language**.
   - The models follow Sokoban rules, simulating player movement, box pushing, and goal completion.
   - Advanced models integrate **static deadlock detection** to identify and eliminate configurations where boxes cannot reach goals, optimizing the state space.

3. **Formal Verification**:
   - The models are executed using **NuXmv**, a symbolic model checker, to verify board solvability.
   - Solvability is determined by checking if a valid sequence of moves exists to push all boxes onto their respective goals.

4. **Automation**:
   - The project includes a script for running multiple solvers on multiple Sokoban boards:
     - **Directory of Solvers**: Specify a directory containing different solver models.
     - **Directory of Boards**: Specify a directory containing Sokoban boards in XSB format.
   - The script:
     - Automatically runs each solver on each board.
     - Collects results, including runtime and solvability status.
     - Outputs a comprehensive summary for easy comparison and analysis.

This framework combines the rigor of formal verification with the flexibility of automation, allowing systematic evaluation of Sokoban boards and solvers. Features like static deadlock detection and multi-solver automation make this project a robust tool for solving and analyzing Sokoban puzzles.

---

## Repository Structure

```plaintext
.
├── models/
│   ├── grid based model/
│   │   ├── Main.py
│   │   ├── extract_moves.py
│   │   ├── run_automation.py
│   │   ├── run_nuXmv.py
│   │   ├── smv_file_generator.py
│   │   ├── sokoban.py
│   │   └── solve_iteratively.py
│   ├── position based model/
│   │   ├── LURD_format_creator.py
│   │   ├── board_assignment.py
│   │   ├── model_generation.py
│   │   ├── run_nuxmv.py
│   │   ├── sokoban.py
│   │   ├── solver.py
│   │   └── solver_iterative.py
│   └── static deadlocks/
│       └── model_generation.py
├── scripts/
│   ├── add_paddings_to_boards.py
│   ├── convertSolutionToExcel.py
│   ├── convert_board_to_mxn.py
│   ├── create_solutions_excel.py
│   ├── create_xsb_files_for_boards.py
│   ├── extractSolutionFile.py
│   ├── extract_board_size.py
│   ├── extract_boards_properties.py
│   └── frame_boards.py
├── run_solvers_directory.py
└── README.md
```
---

## Features

### 1. Multiple Solver Implementations
This project includes three distinct solvers, each providing a unique modeling approach for solving Sokoban puzzles:
- **Grid-Based Model**: 
  - Represents the Sokoban board as a 2D grid and explicitly models player and box movements.
- **Position-Based Model**: 
  - Focuses on the relative positions of boxes and goals, offering a simpler abstraction for certain configurations.
- **Static Deadlocks Model**: 
  - Incorporates static deadlock detection to prevent invalid configurations (e.g., pushing a box into an unreachable position), reducing unnecessary state exploration and improving performance.

### 2. Automated Solver Execution
- Automate the process of running multiple solvers on a directory of Sokoban boards using the `run_solvers_directory.py` script.
- Features:
  - Input: Specify directories containing Sokoban boards (XSB format) and solvers.
  - Output: Collect results such as solvability, runtime, and performance metrics.
  - Summary: Generates a consolidated report for easy comparison and analysis.

### 3. Board Analysis and Preprocessing Tools
The `scripts/` directory provides a suite of utilities for managing and analyzing Sokoban boards:
- **Format Conversion**: Convert Sokoban boards between formats, such as XSB to a matrix-based representation.
- **Board Padding**: Add padding to boards for preprocessing and alignment.
- **Property Extraction**: Analyze board properties such as dimensions and identify static deadlocks.
- **Solution Processing**: Extract, process, and export solver solutions to Excel or other formats for further analysis.

### 4. Formal Verification
- Models are written in the **SMV** language for use with **NuXmv**, a symbolic model checker.
- Verification ensures correctness by systematically exploring the state space to determine solvability.
- Advanced features like static deadlock detection optimize performance by eliminating unsolvable configurations early.

### 5. Extensibility
- Easily add or modify solver implementations to experiment with new approaches or constraints.
- The modular design of the automation and preprocessing scripts makes it easy to adapt to new workflows or integrate into other projects.

### 6. Comprehensive Output
- Generates detailed performance logs, including:
  - Solvability status for each board.
  - Execution time for each solver.
  - Number of moves required to solve a board.
- Outputs results in CSV or Excel formats for easy visualization and comparison.

---

