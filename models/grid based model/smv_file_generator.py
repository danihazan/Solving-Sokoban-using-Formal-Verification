import os
################ SMV FILE GENERATOR ######################
def generate_smv_file(board_file="board_xsb.txt"):
    
    # Create a 2D list from the board text file
    board = create_board_list_from_file(board_file)
    
    # Create the string for the SMV file according to FDS and the winning condition
    smv_string = smv_string_generator(board)

    #Change here your smv file name
    smv_file_name = "sokoban_board_smv_model.smv"
    # Create SMV file 
    with open(smv_file_name, 'w') as file:
        file.write(smv_string)  # Write the string to the file

    print("Your Smv file for this board has been created in .")
    return smv_file_name

    
    

################ XSB BOARD FROM TEXT FILE TO LIST ######################
def create_board_list_from_file(path):
    """
    This function recieves a text file containing a XSB representation of the board 
    and returns a 2D list representing the board
    
    Input:
        path: path to file containing an XSB representation of a sokoban board
    Output:
        board: 2D list representing the board

        """
    valid_characters = {'#', '@', '$', '.', '+', '*', '-'}  # Set of valid XSB Sokoban characters

    with open(path, "r") as smv_model_file:
        board = []  # Initialize an empty list to hold the board
        for line in smv_model_file:
            stripped_line = line.strip()  # Remove leading/trailing whitespace
            if stripped_line:  # Check if the line is not empty
                # Filter out invalid characters and create a list of valid characters
                filtered_line = [char for char in stripped_line if char in valid_characters]
                board.append(filtered_line)  # Add the filtered list of characters to the board

    return board


################ SMV FILE STRING GENERATOR ######################
def smv_string_generator(board):

    """
    This Function creates the content for the smv model file created for the board
    Used for creating the smv file.
    
    Input:
        board: 2D list contsainig the XSB representation of the board
    Output:
        smv_string: string containig the conternt for the smv file
    """
    rows=len(board)
    cols=len(board[0])
    smv_string = f"""
MODULE main
--SMV FILE FOR SOKOBAN BOARD OF SIZE {rows}x{cols}
-- Variables
VAR
    sokoban_board: array 0..{rows-1} of array 0..{cols-1} of {{Wall, Player, POG, Box, BOG, Goal, Floor}};
    move: {{r, l, u, d}}; --direction is non-determinisic
    
-- Initial States
INIT
    {initial_state_string_generator(board)}
    
-- Define transition relations
ASSIGN
    {transition_relation_string_generator(board)}
    
-- solvability function that indica
DEFINE
    is_solvable :=
        {solvability_condition_string_generator(board)}
        
-- check solvability
LTLSPEC !(F is_solvable);

"""

    return smv_string

################ INITIAL STATE STRING ######################
def initial_state_string_generator(board):
    """
    This function creates the string representing the initial state of the board.
    Used for initialization of the model.
    
    Input:
        board: this is a list contsainig the XSB representation of the board
    Output: 
        Outputs a string to use for creating a smv file
        string is the initial state initialization according to board
        xsb to string
        @ = Warehouse Keepr
        + = Warehouse Keeper on Goal
        $ = Box
        * = Box on Goal
        # = Wall
        . = Goal 
        - = Floor
        """
    initialization_string = ''
    row_num=len(board)
    col_num=len(board[0])
    for i in range(row_num):
        for j in range(col_num):
            if(i == row_num-1 and j == col_num-1):
                 #Convert last cell end initializiation
                if board[row_num-1][col_num-1] == '@':
                    initialization_string += f'sokoban_board[{row_num-1}][{col_num-1}] = Player ;\n\t'
                elif board[row_num-1][col_num-1] == '+':
                    initialization_string += f'sokoban_board[{row_num-1}][{col_num-1}] = POG ;\n\t'
                elif board[row_num-1][col_num-1] == '$':
                    initialization_string += f'sokoban_board[{row_num-1}][{col_num-1}] = Box ;\n\t'
                elif board[row_num-1][col_num-1] == '*':
                    initialization_string += f'sokoban_board[{row_num-1}][{col_num-1}] = BOG ;\n\t'
                elif board[row_num-1][col_num-1] == '#':
                    initialization_string += f'sokoban_board[{row_num-1}][{col_num-1}] = Wall ;\n\t'
                elif board[row_num-1][col_num-1] == '.':
                    initialization_string += f'sokoban_board[{row_num-1}][{col_num-1}] = Goal ;\n\t'
                elif board[row_num-1][col_num-1] == '-':
                    initialization_string += f'sokoban_board[{row_num-1}][{col_num-1}] = Floor ;\n\t'

            else:
                                # Convert XSB symbols to string 
                if board[i][j] == '@':
                    initialization_string += f'sokoban_board[{i}][{j}] = Player &\n\t'
                elif board[i][j] == '+':
                    initialization_string += f'sokoban_board[{i}][{j}] = POG &\n\t' 
                elif board[i][j] == '$':
                    initialization_string += f'sokoban_board[{i}][{j}] = Box &\n\t' 
                elif board[i][j] == '*':
                    initialization_string += f'sokoban_board[{i}][{j}] = BOG &\n\t' 
                elif board[i][j] == '#':
                    initialization_string += f'sokoban_board[{i}][{j}] = Wall &\n\t'
                elif board[i][j] == '.':
                    initialization_string += f'sokoban_board[{i}][{j}] = Goal &\n\t'
                elif board[i][j] == '-':
                   initialization_string += f'sokoban_board[{i}][{j}] = Floor &\n\t'

    return initialization_string

################ TRANSITIONS STRING ######################
def transition_relation_string_generator(board):
    """
    This function creates the string to use for model's transitions
    Input:
        board: this is a list contsainig the XSB representation of the board
    Output: 
        String of the transition relations for the board FDS
        will be used for creating the nuxmv file 
    """
    transition_string = ''

    board_rows = len(board)
    board_cols = len(board[0])

#for every cell in the board define next state
    for i in range(board_rows):
        for j in range(board_cols):
            #Wall cells will never change in the game
            
            if board[i][j] == '#':
                transition_string += f'next(sokoban_board[{i}][{j}]) := Wall;\n\t'
            #other cells state may change during the game
            elif board[i][j] == '-' and (i == 0 or j == 0 or i == board_rows - 1 or j == board_cols - 1):
                transition_string += f'next(sokoban_board[{i}][{j}]) := Floor;\n\t'
            else: 
                transition_string += f'next(sokoban_board[{i}][{j}]) := \n\t\tcase\n'
             # -----------------------------------------------------------------------------------------------
                #CURRENT STATE : PLAYER OR POG 
                #Player OR POG moves to Wall
                transition_string += f'\t\t\t--current: Player(@) or POG(+) & move to Wall(#) -> next: Player(@) or POG(+) \n'
                transition_string += f'\t\t\t(sokoban_board[{i}][{j}] = Player | sokoban_board[{i}][{j}] = POG) & move = l & sokoban_board[{i}][{j - 1}] = Wall: sokoban_board[{i}][{j}];\n'
                transition_string += f'\t\t\t(sokoban_board[{i}][{j}] = Player | sokoban_board[{i}][{j}] = POG) & move = r & sokoban_board[{i}][{j + 1}] = Wall: sokoban_board[{i}][{j}];\n'
                transition_string += f'\t\t\t(sokoban_board[{i}][{j}] = Player | sokoban_board[{i}][{j}] = POG) & move = u & sokoban_board[{i - 1}][{j}] = Wall: sokoban_board[{i}][{j}];\n'
                transition_string += f'\t\t\t(sokoban_board[{i}][{j}] = Player | sokoban_board[{i}][{j}] = POG) & move = d & sokoban_board[{i + 1}][{j}] = Wall: sokoban_board[{i}][{j}];\n\n'
                
                
                # PLAYER OR POG MOVES TO BOX OR BOG
                #PLAYER MOVES TO BOX OR BOG BUT IT CANT BE PUSHED
                transition_string += f'\t\t\t--current: Player(@) or POG(+) & move to Box($) or BOG(*) & cant push Box -> next: Player(@) or POG(+) \n'
                if j >= 2:
                    transition_string += (
                        f'\t\t\t(sokoban_board[{i}][{j}] = Player | sokoban_board[{i}][{j}] = POG) & move = l & (sokoban_board[{i}][{j - 1}] = Box | sokoban_board[{i}][{j - 1}] = BOG) & '
                        f'(sokoban_board[{i}][{j - 2}] = Box | sokoban_board[{i}][{j - 2}] = Wall | sokoban_board[{i}][{j - 2}] = BOG) : sokoban_board[{i}][{j}];\n')
                if j < board_cols - 2:
                    transition_string += (
                        f'\t\t\t(sokoban_board[{i}][{j}] = Player | sokoban_board[{i}][{j}] = POG) & move = r & (sokoban_board[{i}][{j + 1}] = Box | sokoban_board[{i}][{j + 1}] = BOG) & '
                        f'(sokoban_board[{i}][{j + 2}] = Box | sokoban_board[{i}][{j + 2}] = Wall | sokoban_board[{i}][{j + 2}] = BOG) : sokoban_board[{i}][{j}];\n')
                if i >= 2:
                    transition_string += (
                        f'\t\t\t(sokoban_board[{i}][{j}] = Player | sokoban_board[{i}][{j}] = POG) & move = u & (sokoban_board[{i - 1}][{j}] = Box | sokoban_board[{i - 1}][{j}] = BOG) & '
                        f'(sokoban_board[{i - 2}][{j}] = Box | sokoban_board[{i - 2}][{j}] = Wall | sokoban_board[{i - 2}][{j}] = BOG) : sokoban_board[{i}][{j}];\n')
                if i < board_rows -2:
                    transition_string += (
                        f'\t\t\t(sokoban_board[{i}][{j}] = Player | sokoban_board[{i}][{j}] = POG) & move = d & (sokoban_board[{i + 1}][{j}] = Box | sokoban_board[{i + 1}][{j}] = BOG) & '
                        f'(sokoban_board[{i + 2}][{j}] = Box | sokoban_board[{i + 2}][{j}] = Wall | sokoban_board[{i + 2}][{j}] = BOG) : sokoban_board[{i}][{j}];\n\n')
                    

            # -----------------------------------------------------------------------------------------------

                #CURRENT STATE : PLAYER 

                #1. Player moves to Goal or Floor
                transition_string += f'\t\t\t--current: Player(@) & move to Goal(.) or Floor(-) -> next: Floor(-) \n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Player & move = l & (sokoban_board[{i}][{j - 1}] = Goal | sokoban_board[{i}][{j - 1}] = Floor) : Floor;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Player & move = r & (sokoban_board[{i}][{j + 1}] = Goal | sokoban_board[{i}][{j + 1}] = Floor) : Floor;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Player & move = u & (sokoban_board[{i - 1}][{j}] = Goal | sokoban_board[{i - 1}][{j}] = Floor) : Floor;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Player & move = d & (sokoban_board[{i + 1}][{j}] = Goal | sokoban_board[{i + 1}][{j}] = Floor) : Floor;\n\n'



                #2. Player moves to BOX
                #PLAYER TRIES TO MOVE TO BOX AND IT CAN BE PUSHED
                transition_string += f'\t\t\t--current: Player(@) & move to Box($) & push Box -> next: Floor(-) \n'
                if j >= 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Player & move = l & (sokoban_board[{i}][{j - 1}] = Box | sokoban_board[{i}][{j - 1}] = BOG) & '
                        f'(sokoban_board[{i}][{j - 2}] = Floor | sokoban_board[{i}][{j - 2}] = Goal): Floor;\n')
                if j < board_cols - 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Player & move = r & (sokoban_board[{i}][{j + 1}] = Box | sokoban_board[{i}][{j + 1}] = BOG) & '
                        f'(sokoban_board[{i}][{j + 2}] = Floor | sokoban_board[{i}][{j + 2}] = Goal): Floor;\n')
                if i  >= 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Player & move = u & (sokoban_board[{i - 1}][{j}] = Box | sokoban_board[{i - 1}][{j}] = BOG) & '
                        f'(sokoban_board[{i - 2}][{j}] = Floor | sokoban_board[{i - 2}][{j}] = Goal): Floor;\n')
                if i  < board_rows - 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Player & move = d & (sokoban_board[{i + 1}][{j}] = Box | sokoban_board[{i + 1}][{j}] = BOG) & '
                        f'(sokoban_board[{i + 2}][{j}] = Floor | sokoban_board[{i + 2}][{j}] = Goal): Floor;\n\n')


                # -----------------------------------------------------------------------------------------------

                #CURRENT STATE : POG 
                #1. PLAYER MOVES TO GOAL OR FLOOR
                transition_string += f'\t\t\t--current: POG(+) & move to Goal(.) or Floor(-) -> next: POG(+) \n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = POG & move = l & (sokoban_board[{i}][{j - 1}] = Goal | sokoban_board[{i}][{j - 1}] = Floor) : Goal;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = POG & move = r & (sokoban_board[{i}][{j + 1}] = Goal | sokoban_board[{i}][{j + 1}] = Floor) : Goal;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = POG & move = u & (sokoban_board[{i - 1}][{j}] = Goal | sokoban_board[{i - 1}][{j}] = Floor) : Goal;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = POG & move = d & (sokoban_board[{i + 1}][{j}] = Goal | sokoban_board[{i + 1}][{j}] = Floor) : Goal;\n\n'



                #2. POG moves to BOX
                #POG TRIES TO MOVE TO BOX AND IT CAN BE PUSHED
                transition_string += f'\t\t\t--current: POG(+) & move to Box($) & push Box -> next: Goal(.) \n'
                if j >= 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = POG & move = l & (sokoban_board[{i}][{j - 1}] = Box | sokoban_board[{i}][{j - 1}] = BOG) & '
                        f'(sokoban_board[{i}][{j - 2}] = Floor | sokoban_board[{i}][{j - 2}] = Goal): Goal;\n')
                if j < board_cols - 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = POG & move = r & (sokoban_board[{i}][{j + 1}] = Box | sokoban_board[{i}][{j + 1}] = BOG) & '
                        f'(sokoban_board[{i}][{j + 2}] = Floor | sokoban_board[{i}][{j + 2}] = Goal): Goal;\n')
                if i  >= 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = POG & move = u & (sokoban_board[{i - 1}][{j}] = Box | sokoban_board[{i - 1}][{j}] = BOG) & '
                        f'(sokoban_board[{i - 2}][{j}] = Floor | sokoban_board[{i - 2}][{j}] = Goal): Goal;\n')
                if i  < board_rows - 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = POG & move = d & (sokoban_board[{i + 1}][{j}] = Box | sokoban_board[{i + 1}][{j}] = BOG) & '
                        f'(sokoban_board[{i + 2}][{j}] = Floor | sokoban_board[{i + 2}][{j}] = Goal): Goal;\n\n')



                # -----------------------------------------------------------------------------------------------

                #CURRENT STATE : GOAL 
                #1. PLAYER/POG MOVES TO GOAL
                transition_string += f'\t\t\t--current: Goal(.) & player move to Goal(.)  -> next: POG(+) \n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Goal & move = l & (sokoban_board[{i}][{j + 1}] = Player | sokoban_board[{i}][{j + 1}] = POG) : POG;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Goal & move = r & (sokoban_board[{i}][{j - 1}] = Player | sokoban_board[{i}][{j + 1}] = POG) : POG;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Goal & move = u & (sokoban_board[{i + 1}][{j}] = Player | sokoban_board[{i}][{j + 1}] = POG) : POG;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Goal & move = d & (sokoban_board[{i - 1}][{j}] = Player | sokoban_board[{i}][{j + 1}] = POG) : POG;\n\n'


                #4.PLAYER PUSHES BOX TO GOAL
                transition_string += f'\t\t\t--current: Goal(.) & player pushes box  -> next: BOG(*) \n'
                if j < board_cols - 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Goal & move = l & (sokoban_board[{i}][{j + 2}] = Player | sokoban_board[{i}][{j + 2}] = POG) & '
                        f'(sokoban_board[{i}][{j + 1}] = Box | sokoban_board[{i}][{j + 1}] = BOG) : BOG;\n')
                if j >= 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Goal & move = r & (sokoban_board[{i}][{j - 2}] = Player | sokoban_board[{i}][{j - 2}] = POG) & '
                        f'(sokoban_board[{i}][{j - 1}] = Box | sokoban_board[{i}][{j - 1}] = BOG) : BOG;\n')
                if i  < board_rows - 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Goal & move = u & (sokoban_board[{i + 2}][{j}] = Player | sokoban_board[{i + 2}][{j}] = POG) & '
                        f'(sokoban_board[{i + 1}][{j}] = Box | sokoban_board[{i + 1}][{j}] = BOG) : BOG;\n')
                if i  >= 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Goal & move = d & (sokoban_board[{i - 2}][{j}] = Player | sokoban_board[{i - 2}][{j}] = POG) & '
                        f'(sokoban_board[{i - 1}][{j}] = Box | sokoban_board[{i - 1}][{j}] = BOG) : BOG;\n\n')
                                     


                # -----------------------------------------------------------------------------------------------
                #CURRENT STATE : FLOOR 
                # 1. PLAYER/POG MOVES TO FLOOR
                transition_string += f'\t\t\t--current: Floor(-) & player move to Floor(-)  -> next: Player(@) \n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Floor & move = l & (sokoban_board[{i}][{j + 1}] = Player | sokoban_board[{i}][{j + 1}] = POG) : Player;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Floor & move = r & (sokoban_board[{i}][{j - 1}] = Player | sokoban_board[{i}][{j - 1}] = POG) : Player;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Floor & move = u & (sokoban_board[{i + 1}][{j}] = Player | sokoban_board[{i + 1}][{j}] = POG) : Player;\n'
                transition_string += f'\t\t\tsokoban_board[{i}][{j}] = Floor & move = d & (sokoban_board[{i - 1}][{j}] = Player | sokoban_board[{i - 1}][{j}] = POG) : Player;\n\n'
                

                #2. PLAYER PUSHES BOX/BOG TO FLOOR 
                transition_string += f'\t\t\t--current: Floor(-) & player pushes box -> next: Box($) \n'
                if j < board_cols - 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Floor & move = l  & (sokoban_board[{i}][{j + 2}] = Player | sokoban_board[{i}][{j + 2}] = POG)& '
                        f'(sokoban_board[{i}][{j + 1}] = Box | sokoban_board[{i}][{j + 1}] = BOG) : Box;\n')
                if j >= 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Floor & move = r & (sokoban_board[{i}][{j - 2}] = Player | sokoban_board[{i}][{j - 2}] = POG) & '
                        f'(sokoban_board[{i}][{j - 1}] = Box | sokoban_board[{i}][{j - 1}] = BOG) : Box;\n')
                if i  < board_rows - 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Floor & move = u & (sokoban_board[{i + 2}][{j}] = Player | sokoban_board[{i + 2}][{j}] = POG) & '
                        f'(sokoban_board[{i + 1}][{j}] = Box | sokoban_board[{i + 1}][{j}] = BOG) : Box;\n')
                if i  >= 2:
                    transition_string += (
                        f'\t\t\tsokoban_board[{i}][{j}] = Floor & move = d & (sokoban_board[{i - 2}][{j}] = Player | sokoban_board[{i - 2}][{j}] = POG) &'
                        f' (sokoban_board[{i - 1}][{j}] = Box | sokoban_board[{i - 1}][{j}] = BOG) : Box;\n\n')


                # -----------------------------------------------------------------------------------------------
                #CURRENT STATE : BOX 
                # 1. PLAYER PUSHES BOX
                transition_string += f'\t\t\t--current: Box($) & player pushes box -> next: Player(@) \n'
                transition_string += (
                    f'\t\t\tsokoban_board[{i}][{j}] = Box & move = l & (sokoban_board[{i}][{j + 1}] = Player | sokoban_board[{i}][{j + 1}] = POG) & '
                    f'(sokoban_board[{i}][{j - 1}] = Floor | sokoban_board[{i}][{j - 1}] = Goal): Player;\n')
                transition_string += (
                    f'\t\t\tsokoban_board[{i}][{j}] = Box & move = r & (sokoban_board[{i}][{j - 1}] = Player | sokoban_board[{i}][{j - 1}] = POG) & '
                    f'(sokoban_board[{i}][{j + 1}] = Floor | sokoban_board[{i}][{j + 1}] = Goal): Player;\n')
                transition_string += (
                    f'\t\t\tsokoban_board[{i}][{j}] = Box & move = u & (sokoban_board[{i + 1}][{j}] = Player | sokoban_board[{i + 1}][{j}] = POG) & '
                    f'(sokoban_board[{i - 1}][{j}] = Floor | sokoban_board[{i - 1}][{j}] = Goal): Player;\n')
                transition_string += (
                    f'\t\t\tsokoban_board[{i}][{j}] = Box & move = d & (sokoban_board[{i - 1}][{j}] = Player | sokoban_board[{i - 1}][{j}] = POG) & '
                    f'(sokoban_board[{i + 1}][{j}] = Floor | sokoban_board[{i + 1}][{j}] = Goal): Player;\n\n')


                # -----------------------------------------------------------------------------------------------
                #CURRENT STATE : BOG
                # 1. PLAYER PUSHES BOG
                transition_string += f'\t\t\t--current: BOG(*) & player pushes box -> next: POG(+) \n'
                transition_string += (
                    f'\t\t\tsokoban_board[{i}][{j}] = BOG & move = l & (sokoban_board[{i}][{j + 1}] = Player | sokoban_board[{i}][{j + 1}] = POG) & '
                    f'(sokoban_board[{i}][{j - 1}] = Floor | sokoban_board[{i}][{j - 1}] = Goal): POG;\n')
                transition_string += (
                    f'\t\t\tsokoban_board[{i}][{j}] = BOG & move = r & (sokoban_board[{i}][{j - 1}] = Player | sokoban_board[{i}][{j - 1}] = POG) & '
                    f'(sokoban_board[{i}][{j + 1}] = Floor | sokoban_board[{i}][{j + 1}] = Goal): POG;\n')
                transition_string += (
                    f'\t\t\tsokoban_board[{i}][{j}] = BOG & move = u & (sokoban_board[{i + 1}][{j}] = Player | sokoban_board[{i + 1}][{j}] = POG) & '
                    f'(sokoban_board[{i - 1}][{j}] = Floor | sokoban_board[{i - 1}][{j}] = Goal): POG;\n')
                transition_string += (
                    f'\t\t\tsokoban_board[{i}][{j}] = BOG & move = d & (sokoban_board[{i - 1}][{j}] = Player | sokoban_board[{i - 1}][{j}] = POG) & '
                    f'(sokoban_board[{i + 1}][{j}] = Floor | sokoban_board[{i + 1}][{j}] = Goal): POG;\n\n')



                 # *********************************************************************************************
                 # *********************************************************************************************
                 # *********************************************************************************************


 

                # DEFAULT CASE
                transition_string += f'\n\t\t\t-- Default case\n'
                transition_string += f'\t\t\tTRUE: sokoban_board[{i}][{j}];\n'
                transition_string += f'\t\tesac;\n'
                transition_string += '\n\t\t'

    return transition_string

################ IS SOLVABLE CONDITION STRING ######################
def solvability_condition_string_generator(board):
    """
        Input:
        board: this is a list contsainig the XSB representation of the board
    Output: 
        Generate the string describing the winning condition
    
    """
    solvability_condition = ''

    goal_counter=0
    # Find number of Goals on board (BOG,POG,GOAL)
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '.' or board[i][j] == '+' or board[i][j] == '*': #GOAL or POG or BOG
                goal_counter+=1
    counter=0
    # Generate String to define solvability- check if all goals are BOG
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '.' or board[i][j] == '+' or board[i][j] == '*': #GOAL or POG or BOG
                    counter+=1
                    if counter < goal_counter:
                        solvability_condition += f'sokoban_board[{i}][{j}] = BOG & \n\t'  # Not the last '.' in the board
                    elif counter==goal_counter:
                        solvability_condition += f'sokoban_board[{i}][{j}] = BOG ;\n'  # Last '.' in the board
                        break
        if counter==goal_counter:
            break
    return solvability_condition

def write_to_file(path, smv_string):
    """
    input: path: the path to the file where the SMV model will be written.
    param smv_string: the SMV model as a string to be written to the file.
    output: write the smv_string to the file in path
    """
    with open(path, "w") as smv_model_file:
        smv_model_file.write(smv_string)





