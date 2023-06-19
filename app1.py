import subprocess
import json
import random
import string
import time


def execute_command_with_retry(command):
    max_retries = 3
    retry_delay = 1

    retries = 0
    while retries < max_retries:
        try:
            # Attempt to execute the command
            return subprocess.check_output(command).decode().strip()
            # Perform further operations if the command executes successfully
        except subprocess.CalledProcessError as e:
            # Handle the CalledProcessError exception
            print("Error executing command:", e)
            # Perform error handling operations

            # Wait for 1 second before retrying
            time.sleep(retry_delay)
            retries += 1

    print("Maximum retries exceeded. Failed to execute the command.")


# Create enum for the strategy
class StrategyEnum:
    RANDOM = "random"
    SUCCESS = "success"
    FAILURE = "failure"


strategy = StrategyEnum.SUCCESS


def invoke_function(input):
    # Invoke the target function in OpenWhisk
    # Pass the input as a parameter to the function
    # Return the output or any relevant feedback
    command = ["wsk", "action", "invoke", "md5", "--param", "input", input]

    output = execute_command_with_retry(command)

    # split the string and get last string
    activation_id = output.split(" ")[-1]
    # sleep for 1 seconds
    time.sleep(1)

    activation_command = ["wsk", "activation", "get", activation_id]
    result = execute_command_with_retry(activation_command)
    # result = subprocess.check_output(activation_command).decode().strip()

    # add try catch and catch CalledProcessError

    # split the string and remove the data before {, the string should include {

    result_from = result.split("{", 1)[1]
    result_from = str("{") + str(result_from)

    # Parse the output as a JSON object
    json_data = json.loads(result_from)

    return json_data


def generate_input():
    # Generate or mutate a test input based on the current strategy
    # For simplicity, this example generates a random string
    if strategy == StrategyEnum.FAILURE:
        return generate_random_string_with_errors(50)
    elif strategy == StrategyEnum.SUCCESS:
        return generate_random_string_with_success(50)
    else:
        return generate_random_string(50)


def generate_random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_random_string_with_errors(length):
    # Generate a random string with errors based on specific strategy

    # Choose a random index to introduce an error
    error_index = random.randint(0, length - 1)

    # Generate a random string of given length
    chars = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(chars) for _ in range(length))

    # Introduce an error at the randomly chosen index
    error_char = random.choice(chars)
    mutated_string = random_string[:error_index] + error_char + random_string[error_index + 1:]

    return mutated_string


def read_check_already_string(gen_str):
    # file success.txt file and get all string as array and check if the gen_str is already in the array
    data = []
    with open('success.txt') as f:
        temp = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        data = [x.strip() for x in temp]

    if gen_str in data:
        return True
    else:
        return False


def generate_random_string_with_success(length):
    # Generate a random string with success based on a specific strategy

    # Choose a random index to highlight success
    success_index = random.randint(0, length - 1)

    # Generate a random string of given length
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_-+=[]{}|;:,.<>?"
    random_string = ''.join(random.choice(chars) for _ in range(length))
    success_char = random.choice(chars)

    mutated_string = random_string[:success_index] + success_char + random_string[success_index + 1:]

    # Mutate the string
    mutation_index = random.randint(0, length - 1)
    mutation_char = random.choice(chars)
    mutated_string = mutated_string[:mutation_index] + mutation_char + mutated_string[mutation_index + 1:]

    if not read_check_already_string(mutated_string):
        return generate_random_string(length)

    return mutated_string


def update_strategy(output):
    # check if the output is true or false
    if output['response']['result'] == True:
        print("Long output detected. Adjusting mutation strategy for longer outputs...")
        strategy = StrategyEnum.SUCCESS
    else:
        strategy = StrategyEnum.FAILURE


def fuzzing_loop():
    start_time = time.time()
    duration = 500  # 5 seconds

    # Fuzzing loop to generate test inputs and invoke the function
    while time.time() - start_time < duration:
        # Generate or mutate a test input
        input_data = generate_input()

        # Invoke the function with the input
        output = invoke_function(input_data)

        # Process the feedback and update the test input generation strategy
        update_strategy(output)

        # Log the input output
        if strategy == StrategyEnum.SUCCESS:
            # Save the input to a file
            with open("success.txt", "a") as file:
                file.write(input_data + "\n")

        elif strategy == StrategyEnum.FAILURE:
            with open("error.txt", "a") as file:
                file.write(input_data + "\n")


if __name__ == "__main__":
    # Start the fuzzing loop
    fuzzing_loop()
