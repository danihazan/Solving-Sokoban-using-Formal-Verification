import glob
import shutil
import subprocess
import os
import psutil
import time
import psutil
import threading
import time
import stat




def run_nuXmv_solver(solver_path, board_path, output_file,time_limit, iterative_mode=False, bdd=False,steps=None):
    """
    Runs nuXmv solvers exe file
    parameters accepted:
    -ITERATIVE True
    -BDD True
    -STEPS number
    """
    print(f"solver_path={solver_path} board_path={board_path} outputfile={output_file} time_limit={time_limit} nuXmv iterative mode= {iterative_mode} bdd= {bdd} steps= {steps} ...")
    if not os.path.isfile(solver_path):
        print(f"File not found: {solver_path}")
        return
    #append running Mode command line
    command = [solver_path, board_path]
    if iterative_mode:
        command.append('-ITERATIVE')
        command.append('True')
    if bdd:
        command.append('-BDD')
        command.append('True')
    if steps is not None:
        command.extend(['-STEPS', str(steps)])  # Ensure steps is always a string

    try:
        # Start the process and enforce a timeout with communicate()
        start_time = time.time()  # Start time
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ps_process = psutil.Process(process.pid)  # Get the psutil process object
        peak_memory_usage = [0]  # Use a list to hold peak memory usage (allows modification in a thread)

        # Start memory monitoring in a separate thread
        memory_thread = threading.Thread(target=monitor_memory, args=(ps_process, peak_memory_usage))
        memory_thread.start()

        try:
            # Capture the output and error (if any) from the process with a timeout
            stdout, stderr = process.communicate(timeout=time_limit)
            return_code = process.returncode
        except subprocess.TimeoutExpired:
            print("The command exceeded the timeout of 1.5 Hour and was terminated.")
            
            # Kill the process and any child processes
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()

            with open(output_file, 'a') as f:
                f.write(f"\n--- Running Solver {solver_path} ---\n")
                f.write("nuXmv Solver cannot solve this board in time limit.\n")
                f.write(f"BDD: {bdd} Iterative Mode: {iterative_mode} steps:{steps}\n")
                f.write(f"Peak Memory Usage: {peak_memory_usage[0]:.2f} MB\n")
            return  -1# Exit the function

        memory_thread.join()  # Ensure the memory monitoring thread has finished
        end_time = time.time()  # End time
        elapsed_time = end_time - start_time  # Calculate the elapsed time

        if return_code != 0:
            print(f"Errors from the nuXmv_solver.exe:\n{stderr}")
        else:
            with open(output_file, 'a') as f:
                f.write(f"\n--- Running Solver {solver_path} ---\n")
                f.write(stdout if stdout else 'No output received.\n')
                f.write(f"Peak Memory Usage: {peak_memory_usage[0]:.2f} MB\n")
                f.write(f"Running Time: {elapsed_time:.5f} seconds\n")
            print(f"Output from the {solver_path}:\n{stdout if stdout else 'No output received.'}")
            print(f"Peak Memory Usage: {peak_memory_usage[0]:.2f} MB")
            print(f"Running Time: {elapsed_time:.5f} seconds")
            

    except Exception as e:
        print(f"Failed to run the {solver_path}: {e}")
    return 0
    


def runSolvers(board_path,directory_path,output_file,time_limit,iterative_mode=False,bdd=True,steps=None):
    
        # Iterate through each file in the given directory
    for filename in os.listdir(directory_path):
        # Check if the file is a .exe file
        if filename.endswith(".exe"):
            solver_path = os.path.join(directory_path, filename)
            print(f"\n--- Running Solver {filename} ---\n")
            
            run_nuXmv_solver(solver_path,board_path,output_file,time_limit,iterative_mode,bdd,steps)
            print(solver_path)
            print(board_path)
            print()
    
        board_directory=os.path.dirname(board_path)
        remove_files_with_pattern(board_directory,".out")
        remove_files_with_pattern(board_directory,".smv")
        remove_files_with_pattern(board_directory,".log")
        remove_non_solution_folders(board_directory)

def runSolversForDirectory(board_directory,directory_path,time_limit,iterative_mode=False,bdd=True,steps=None):
    
    # Define the board directory and solutions directory
    board_path_dir = os.path.join('boards', board_directory)
    solutions_dir = os.path.join(board_path_dir, 'solutions')
    
    # Create the solutions directory if it doesn't exist
    if not os.path.exists(solutions_dir):
        os.makedirs(solutions_dir)
        
    # Iterate over all files in the board directory
    for board_file in os.listdir(board_path_dir):
        # Process only files with .txt extension (you can modify the filter as needed)
        if board_file.endswith('.xsb' or '.txt'):
            board_path = os.path.join(board_path_dir, board_file)

            # Define the output file name and path
            output_file_name = f"{os.path.splitext(board_file)[0]}_output.txt"
            output_file = os.path.join(solutions_dir, output_file_name)

            # Run the solvers for this board file
            runSolvers(board_path, directory_path, output_file, time_limit, iterative_mode,bdd,steps)
    
def runSolversForSingleBoard(board_directory,board_file,directory_path,time_limit,iterative_mode=False,bdd=True,steps=None):
    board_path=os.path.join('boards',board_directory, board_file)
    # Define the solutions directory
    solutions_dir = os.path.join('boards', board_directory, 'solutions')

    # Create the solutions directory if it doesn't exist
    if not os.path.exists(solutions_dir):
        os.makedirs(solutions_dir)

    # Define the output file name and path
    output_file_name = f"{os.path.splitext(board_file)[0]}_output.txt"
    output_file = os.path.join(solutions_dir, output_file_name)
    runSolvers(board_path, directory_path, output_file, time_limit, iterative_mode,bdd,steps)



def remove_non_solution_folders(parent_directory):
    """
    Removes all directories within the specified parent_directory that are not named 'solutions'.
    """
    try:
        # List all entries in the directory
        for entry in os.listdir(parent_directory):
            entry_path = os.path.join(parent_directory, entry)
            
            # Check if it is a directory and not named 'solutions'
            if os.path.isdir(entry_path) and entry.lower() != 'solutions':
                try:
                    # Try changing permissions to avoid access issues
                    os.chmod(entry_path, stat.S_IWUSR)  # Set write permission to the user
                    shutil.rmtree(entry_path, onerror=on_rm_error)
                    print(f"Removed folder: {entry_path}")
                except Exception as e:
                    print(f"Failed to remove folder {entry_path}: {e}")
            elif os.path.isdir(entry_path) and entry.lower() == 'solutions':
                print(f"Skipped folder: {entry_path}")

    except Exception as e:
        print(f"An error occurred: {e}")



def on_rm_error(func, path, exc_info):
    """
    Error handler for removing read-only files.
    """
    if not os.access(path, os.W_OK):  # If the file is not writable
        os.chmod(path, stat.S_IWUSR)  # Add write permission and retry
        func(path)
    else:
        raise exc_info[1]  # Re-raise the original exception if it wasn't a permission error


def monitor_memory(ps_process, peak_memory):
    """ Monitors memory usage of the process and updates peak_memory """
    try:
        while ps_process.is_running():
            try:
                memory_info = ps_process.memory_info()
                memory_used = memory_info.rss / (1024 ** 2)  # Convert to MB
                peak_memory[0] = max(peak_memory[0], memory_used)

                # Check child processes
                for child in ps_process.children(recursive=True):
                    child_memory_info = child.memory_info()
                    child_memory_used = child_memory_info.rss / (1024 ** 2)
                    peak_memory[0] = max(peak_memory[0], child_memory_used)

                time.sleep(0.1)  # Check every 100ms
            except psutil.NoSuchProcess:
                break  # Process has terminated
    except Exception as e:
        print(f"Error in memory monitoring: {e}")
        
def remove_files_with_pattern(directory, pattern):
    """
    Removes files from the specified directory that contain the given pattern in their name.
    
    :param directory: The directory to search for files.
    :param pattern: The pattern to look for in file names.
    """
    # Create the search pattern
    search_pattern = os.path.join(directory, f"*{pattern}*")

    # Find all files matching the pattern
    files_to_remove = glob.glob(search_pattern)

    # Remove each file
    for file_path in files_to_remove:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Failed to remove {file_path}: {e}")


def main():
    # Path to the Sokoban board file and output file
    board_directory='report_boards'
    
    # Path to Solvers Directory
    solver_directory='exe'
    
    #timelimit [seconds]
    time_limit=3600
    
    #iterative mode
    iterative_mode= False
    
    # bdd Engine
    bdd= True
    
    #steps bmc
    steps = None
    
    single_board=True
    if single_board==True:
        # Run Solvers for single board
        board_file='board30.xsb'
        runSolversForSingleBoard(board_directory,board_file,solver_directory, time_limit, iterative_mode,bdd,steps)
    else:
        # Run Solvers for directory
        runSolversForDirectory(board_directory,solver_directory, time_limit, iterative_mode,bdd,steps)
    
    

if __name__ == "__main__":
    main()


