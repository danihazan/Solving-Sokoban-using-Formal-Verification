import subprocess
import sys

def run_executable(iterative_mode=False, engine=None, steps_num=None, output_file='output.txt'):
    # Construct the command
    command = ['sokoban_solver.exe']
    
    if iterative_mode:
        command.append('--iterative_mode')
        command.append('True')
    else:
        command.append('--iterative_mode')
        command.append('False')
        
    if engine is not None:
        command.append('--engine')
        command.append(engine)
        
    if steps_num is not None:
        command.append('--steps_num')
        command.append(str(steps_num))
        
    # Print the command to see what will be executed
    print('Running command:', ' '.join(command))
    
    # Open the output file
    with open(output_file, 'w') as f:
        # Execute the command and redirect the output to the file
        try:
            result = subprocess.run(command, stdout=f, stderr=subprocess.PIPE, text=True)
            # Check if there are any errors and print them
            if result.stderr:
                print('Errors:')
                print(result.stderr)
                # Optionally, you can also write errors to the file
                with open(output_file, 'a') as error_file:
                    error_file.write('\nErrors:\n')
                    error_file.write(result.stderr)
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    # Example usage
    run_executable(iterative_mode=True, engine='SAT', steps_num=50, output_file='output.txt')

if __name__ == "__main__":
    main()
