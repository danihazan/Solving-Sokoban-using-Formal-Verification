import os

def extract_moves_from_output_file(output_filename):
    """
    This file extracts the winning path from the model nuXmv output.
    
    Input:
        output_filename: name of the output file from the smv run    
    Output:
        path_to_win: list containig the players moves (in LURD format) leading to winning state(all boxes on goals)

    """
    
#Extract moves from 
    move = None
    is_move = False # this variable checks if last line before condition is true is move
    path_to_win = []
    try:
        with open(output_filename, 'r') as file:
            for line in file:
                #is_move = False
                if "State" in line:
                    # insert move to list
                    if move is not None:
                        path_to_win.append(move)
                elif "move =" in line:
                    #is_move = True
                    move = line.split('=')[-1].strip()#extract player's move from line
                elif "is_solvable = TRUE" in line:
                    break
        return path_to_win

    except FileNotFoundError:
        print(f"The file {output_filename} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

