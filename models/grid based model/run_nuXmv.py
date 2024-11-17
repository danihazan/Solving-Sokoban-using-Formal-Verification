import subprocess
import os
import time
def run_nuxmv(smv_file_name, engine_type=None,steps_number=None):
    """

    This file runs the .smv file that was created by the smv_file generator.
    
    Input:
        smv_file_name: name of the .smv file that was created by the generator(or any file modeling a sokobab board)
        steps_number: In case user wants to limit number of steps for player (defaults to no limit)
        engine_type type= engine for model checking - BDD / SAT / None (default Model checking)
    
    Output:
        This function returns the name of the output file of the run
        For SAT and BDD engine print simulation time

    """
    try:
        engine_string = ""
        #Model Checking
        if engine_type == None:
            # Run the command
            # nuXmv filename
            nuxmv_process = subprocess.Popen(["nuXmv", smv_file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
            stdout, _ = nuxmv_process.communicate()

        #SAT Solver EngineS
        
        elif engine_type == "SAT":
            print("Running smv file with SAT Engine .")
            simulation_start = time.time()
            # Start the nuXmv process in interactive mode
            nuxmv_process = subprocess.Popen(
                ["nuXmv", "-int", smv_file_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            # Send SAT based commands to the nuXmv process
            if steps_number == None:
                commands = "go\ncheck_ltlspec\nquit\n"

            else:
                commands = f"go_bmc\ncheck_ltlspec_bmc -k {steps_number}\nquit\n"
            stdout, _ = nuxmv_process.communicate(input=commands)
            simulation_end = time.time()
            simulation_time = simulation_end - simulation_start
            print(f"Simulation running time for SAT engine:{simulation_time}")
            engine_string="_SAT"

        #BDD Engine 
        elif engine_type == "BDD":
            print("Running smv file with BDD Engine .")
            simulation_start = time.time()
            # Start the nuXmv process in interactive mode
            nuxmv_process = subprocess.Popen(
                ["nuXmv", "-int", smv_file_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Send BDD based commands to the nuXmv process
            commands = f"go\ncheck_ltlspec\nquit\n"
            stdout, _ = nuxmv_process.communicate(input=commands)
            #Calculate run time
            simulation_end = time.time()
            simulation_time = simulation_end - simulation_start 
            print(f"Simulation running time for BDD engine:{simulation_time}")
            engine_string="_BDD"


        # SAVE Output 
        # Wait for the process to complete and capture the output
        output_filename = smv_file_name.split(".")[0] + engine_string + ".out"

        # Save output to file
        with open(output_filename, "w") as f:
            f.write(stdout)
        print(f"Output saved to {output_filename}")


        return output_filename
    except Exception as e:
        return None, f"An error occurred: {e}"

    