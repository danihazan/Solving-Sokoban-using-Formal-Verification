import sys
import time
import smv_file_generator
import run_nuXmv
import extract_moves
import solve_iteratively
import os
import argparse

def main(board_path='boards/board6.txt',iterative_mode = False , engine = 'BDD' , steps_num = None):
    #UPDATE BOARD FILE HERE
    if(iterative_mode):
        solve_iteratively.solve_sokoban_iteratively(board_path, engine, steps_num)
    else:
        #Generate smv file from board
        smv_file_name=smv_file_generator.generate_smv_file(board_path)
        print("The file has been created and the content has been written.")
        #Run Smv file using script
        output_file_name=run_nuXmv.run_nuxmv(smv_file_name,engine,steps_num)

        #Extract path to winning state
        winning_path=extract_moves.extract_moves_from_output_file(output_file_name)

        #Print results
        if len(winning_path) == 0 and engine == "SAT" and steps_num != None:
            print(f"No solution for this board in {steps_num} steps.")      
        elif len(winning_path) == 0:
            print("There is no solution for this board, Board unsolvable.")
        else:
            print(f"Path to win: {winning_path}.")

if __name__ == "__main__":
    main('boards/board_54X Sharpen.txt', False, "BDD")

'''  
    parser = argparse.ArgumentParser(description="Sokoban Solver")

    # Required positional argument for the board path
    parser.add_argument('board_path', type=str, help='Path to the board file')

    # Optional arguments with enforced choices
    parser.add_argument('-ITERATIVE', '--iterative_mode', type=str, choices=['True', 'False'], default='False', help='Enable iterative mode (true or false)')
    parser.add_argument('-ENGINE', '--engine', type=str, choices=['SAT', 'BDD'], default=None, help='Specify the engine to use (SAT or BDD)')
    parser.add_argument('-STEPS', '--steps_num', type=int, default=None, help='Specify the number of steps (integer)')

    args = parser.parse_args()

    # Convert 'true'/'false' string to a boolean
    iterative_mode = args.iterative_mode.lower() == 'true'

    # Call main with the parsed arguments
    main(args.board_path, iterative_mode, args.engine, args.steps_num)
'''

"""
Examples of how to run : 
Scenario 1: Running with All Arguments
nuXmv_solver.exe "boards/original plus extra/board_1.xsb" -ITERATIVE true -ENGINE SAT -STEPS 100

Scenario 2: Running with Only the Required Argument
nuXmv_solver.exe "boards/original plus extra/board_1.xsb"

Scenario 3: Running with a Different Engine and No Steps Specified
nuXmv_solver.exe "boards/original plus extra/board_1.xsb" -ITERATIVE true -ENGINE BDD

Scenario 4: Running with Iterative Mode Disabled Explicitly
nuXmv_solver.exe "boards/original plus extra/board_1.xsb" -ITERATIVE false -ENGINE SAT

"""