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


