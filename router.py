import subprocess
import sys
import time
import select

from simulation import read_hardware_state, write_hardware_state, calculate_f, mutate_hardware, mutate_database, create_hardware_file, file_path

def print_cli_history(history):
    for entry in history:
        print(entry)

def process_cli_input(file_path, history, t):
    # Process CLI input here
    try:
        user_input = input("Enter CLI command: ")
        command, *args = user_input.split()
        if command == "set":
            index = int(args[0]) - 1
            value = int(args[1])
            if index < 0 or index >3 :
                print(f"Invalid Input - Error: {index}")
            else:
                mutate_database(file_path, index, value)
                history.append(f"{t} set {index} {value}")
    except Exception as e:
        print(f"Invalid Input - Error: {str(e)}")

def main():
    history = []
    t = 0


    while t < 60:
        state_values, control_values, signal_values = read_hardware_state(file_path)
        t += 1

        # Write Your Code Here Start

        if t % 10 == 0:
            # Swap state values at indices 1 and 2 (1-indexed)
            state_values[0], state_values[1] = state_values[1], state_values[0]
            # Write the updated state values back to the hardware file
            write_hardware_state(file_path, state_values, control_values, signal_values)
            history.append(str(t) + " swap " + str(state_values[0]) + " " + str(state_values[1]))

        control_values[signal_values[0] - 1] = signal_values[1]
        write_hardware_state(file_path, state_values, control_values, signal_values)

        # Use select to check for input
        print("> ", end="", flush=True)
        
        # Monitor sys.stdin for input
        readable, _, _ = select.select([sys.stdin], [], [], 100)
        
        if readable:
            # Read the user input from stdin
            user_input = sys.stdin.readline().strip()

            # Exit if the user types "exit"
            if user_input.lower() == "exit":
                print("Exiting CLI.")
                sys.exit(0)
            
            # If input is not empty, parse and execute
            if user_input:
                # Split the input into parts (e.g., ["set", "j", "k"])
                parts = user_input.split(" ")

                if parts[0].lower() == "set" and len(parts) == 3:
                    # Handle the "set" command
                    j = int(parts[1])
                    k = int(parts[2])

                    control_values[j - 1] = k
                    write_hardware_state(file_path, state_values, control_values, signal_values)

                    history.append(str(t) + " set " + str(j) + " " + str(k))

                else:
                    print("Invalid command or incorrect number of arguments.")
            else:
                print("Please enter a valid command.")
        else:
            # If no input, continue to the next iteration
            continue

        # Write Your Code Here End

        time.sleep(1)  # Wait for 1 second before polling again
        print(history)

if __name__ == '__main__':
    main()