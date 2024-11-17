from smv_file_generator import *
import time
import run_nuXmv
import re

SYMBOL_MAPPING = {
    'Wall': '#',
    'Player': '@',
    'POG': '+',
    'Box': '$',
    'BOG': '*',
    'Goal': '.',
    'Floor': '-'
}

def extract_lines_between_states(nuXmv_output):
    """
    This function processes a string output from the nuXmv model checker,
    extracting and yielding lists of lines that occur between "State" markers.

    Input:
        A single string (nuXmv_output) containing the output from nuXmv,
        with each line separated by a newline character (\n).

    Output:
        A generator that yields lists of lines found between occurrences of lines containing the word "State".
        Each yielded list represents the lines between consecutive "State" markers in the input.

    """

    lines_between = []
    is_between_states = False

    for output_line in nuXmv_output.split('\n'):
        if 'State' in output_line:
            if not is_between_states:
                lines_between = []
                is_between_states = True
            else:
                yield lines_between
                lines_between = []
        elif is_between_states:
            lines_between.append(output_line)

    if is_between_states:
        yield lines_between


def extract_goal_positions(sokoban_board_file):

    """
    This function processes a Sokoban board file to identify the positions of goal cells
    and returns these positions along with the board representation.

    Input:
        A file path (sokoban_board_file) containing the Sokoban board.

    Output:
        goal_positions: A list of tuples representing the row and column indices of goal positions on the board.
        board_lines: A list of strings where each string represents a line from the board file.
     """

    goal_positions = []
    board_lines = create_board_list_from_file(sokoban_board_file)

    for row_index, line in enumerate(board_lines):
        for col_index, cell in enumerate(line):
            if cell in ['.', '+', '*']:
                goal_positions.append((row_index, col_index))

    return goal_positions, board_lines

def identify_changes(state_lines):
    """
    This function processes lines representing states in a Sokoban board and
    identifies changes in the board state, excluding walls, returning a list of these changes.


    Input:
        A list of strings (state_lines) where each string represents a line from the state description of the Sokoban board.
    Output:
        changes_list: A list of lists, where each inner list contains tuples.
        Each tuple represents a change in the board state,
        extracted from the state lines, in the form of row index,
        column index, and the new state of the cell.

"""
    changes_list = []

    for state_line in state_lines:
        if "sokoban_board" in state_line and "Wall" not in state_line:
            changes_list.append(re.findall(r'\[([0-9]+)\]\[([0-9]+)\] = (\w+)', state_line))

    return changes_list


def generate_smv(sokoban_goals, board_data):

    """
    This function generates an SMV (Symbolic Model Verification) model for a Sokoban board, including its initial state,
    transition rules, and solvability conditions, and returns the resulting SMV model as a string.

    Input:
        sokoban_goals: A list of goal positions on the Sokoban board (not explicitly used in the function).
        board_data: A list of lists representing the Sokoban board, where each inner list corresponds to a row of the board.
    Output:
        smv_text: A string containing the SMV model for the given Sokoban board,
        including module definitions, initial state,
        transition rules, solvability conditions, and an LTL (Linear Temporal Logic) specification for checking unsolvability.

    """

    board_rows = len(board_data)
    board_cols = len(board_data[0])

    initial_state = initial_state_string_generator(board_data)
    transition_rules = transition_relation_string_generator(board_data)
    solvability_conditions = solvability_condition_string_generator(board_data)

    smv_text = f"""
    MODULE main
    VAR
        sokoban_board: array 0..{board_rows - 1} of array 0..{board_cols - 1} of {{Wall, Player, POG, Box, BOG, Goal, Floor}};
        move: {{r, l, u, d}};

    INIT
        {initial_state}

    ASSIGN
        {transition_rules}

    DEFINE
        is_solvable :=
            {solvability_conditions}

    LTLSPEC !(F is_solvable);
    """
    return smv_text


def update_initial_state(current_board, output_filename):

    """
    This function updates the initial state of a Sokoban board based on state changes extracted from
    a specified output file and returns the updated board.

    Input:
        current_board: A list of lists representing the current state of the Sokoban board.
        output_filename: A string representing the path to the file containing the output data.
    Output:
        An updated list of lists representing the Sokoban board after applying the state changes,
        or -1 if the 'State' marker is not found in the file.
    """

    with open(output_filename, "r") as file:
        final_output = file.read()

    if 'State' not in final_output:
        return -1
    else:
        state_data = final_output[final_output.index('State'):]

    for state_lines in extract_lines_between_states(state_data):
        positions_to_update = identify_changes(state_lines)
        positions_to_update = [position[0] for position in positions_to_update]

    for pos in positions_to_update:
        row, col = int(pos[0]), int(pos[1])
        current_board[row][col] = SYMBOL_MAPPING[pos[2]]

    return current_board

def solve_sokoban_iteratively(board_file, engine = None, k = None ):

    """
    This function solves a Sokoban board iteratively by adding one goal at a time, running the nuXmv model checker,
    and updating the board state. It returns the times taken for each iteration.

    Input:
        board_file: A string representing the path to the Sokoban board file.
        engine (optional): An engine parameter for the nuXmv model checker.
        k (optional): A parameter for the nuXmv model checker.
    Output:
        iteration_times: A list of tuples where each tuple contains the time taken for an iteration and the corresponding iteration number.

    """

    simulation_start = time.time()
    board_name = board_file.split(".")[0]
    goals, initial_board = extract_goal_positions(board_file)

    iteration_times = []
    current_goals = []

    for index, goal in enumerate(goals):
        current_goals.append(goal)
        smv_file_content = generate_smv(current_goals, initial_board)


        with open(f"{board_name}_goals{index}.smv", 'w') as smv_file:
            smv_file.write(smv_file_content)

        start_time = time.time()
        output_filename = run_nuXmv.run_nuxmv(f"{board_name}_goals{index}.smv", engine, k)
        print("Running nuXmv on file:", f"{board_name}_goals{index}.smv")
        end_time = time.time()

        iteration_times.append((end_time - start_time, index + 1))
        initial_board = update_initial_state(initial_board, output_filename)
        #print("Iteration complete, time taken:", end_time - start_time)
        if initial_board == -1:
            print("No solution for this board configuration.")
            return []

    # Calculate run time
    simulation_end = time.time()
    simulation_time = simulation_end - simulation_start

    print(f"Simulation running time: {simulation_time:.3f} seconds")
    print(f"Total number of iterations: {len(iteration_times)}")
    return iteration_times
