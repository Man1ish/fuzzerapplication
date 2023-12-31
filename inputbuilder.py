import json
import string
import random
import pandas as pd

class InputReader:
    def command(self):
        pass

    def process(self):
        pass


class InvokeInput(InputReader):

    def __init__(self, given_input, generate=False,execution_time_function=0,memory_used=0,last_code_coverage =0):
        self.given_input = given_input
        self.success_file = "output/invoke.txt"
        self.error_file = "output/error.txt"
        self.execution_time_file = "output/execution.txt"
        self.metrics_file = "output/metrices.txt"
        self.last_code_coverage = last_code_coverage
        self.best_code_coverage = 0
        if generate:
            self.method_name = "md5"
            self.input = self.generate_mutated_string(30,execution_time_function,memory_used)
        else:
            self.method_name, self.input = self.extract_input()

    def save_execution_time(self, execution_time):
        with open(self.execution_time_file, "a") as myfile:
            myfile.write(str(execution_time) + "\n")


    def save_metrics(self,docker_name, language, memory_used,execution_time_function, error, count):
        with open(self.metrics_file, "a") as myfile:
            myfile.write(str(docker_name)+","+str(language)+","+str(memory_used)+","+str(execution_time_function)+","+str(error)+","+ str(count)+ "\n")

    def minimum_no_of_error(self):
        return 0

    def minimum_no_of_logs(self):
        return 16

    def extract_input(self):
        array = self.given_input.split(',')
        return array[0], array[1]

    def command(self):
        my_array = ["wsk", "action", "invoke", self.method_name, "--param", "input", self.input, "--result"]
        my_string = ' '.join(my_array)
        print(my_string)
        return my_array

    def write_output_message(self,count,error,memory,name,memory_assign,language):
        print("="* 80)
        if memory_assign > 0:
            print("Code reached: "+str(count) + ", Error count: "+str(error)+", Memory used: "+str(memory)+", Docker name: "+str(name.replace(".txt", ""))
                  +" Memory assign: "+str(memory_assign)+", Language: "+str(language.replace("md5.", "")))
        else:
            print("Code reached: "+str(count) + ", Error count: "+str(error)+", Memory used: "+str(memory)
                  +", Docker name: "+str(name.replace(".txt", ""))+", Language: "+str(language.replace("md5.", "")))


    def process(self):
        pass

    def compile_result(self, result):
        json_data = json.loads(result)
        return True

    def generate_random_string(self, length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def read_check_already_string(self, gen_str):
        # file success.txt file and get all string as array and check if the gen_str is already in the array
        data = []

        with open(self.success_file) as f:
            temp = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            data = [x.strip() for x in temp]

        if gen_str in data:
            return True
        else:
            return False

    def get_updated_memory(self):
        return random.randint(128, 256)

    def get_create_file_name(self):
        my_list = ["md5.py", "md5.js"]
        # random_element = random.choice(my_list)
        return random.choice(my_list)

    def generate_mutated_string(self, length,execution_time,memory):
        # Generate a random string with success based on a specific strategy


        # Choose a random index to highlight success
        success_index = random.randint(0, length - 1)

        # Generate a random string of given length
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_-+=[]{}|;:,.<>?"

        random_string = ''.join(random.choice(chars) for _ in range(length))
        success_char = random.choice(chars)

        mutated_string = random_string[:success_index] + success_char + random_string[success_index + 1:]

        mutation_index = random.randint(0, length - 1)
        mutation_char = random.choice(chars)
        mutated_string = mutated_string[:mutation_index] + mutation_char + mutated_string[mutation_index + 1:]
        mutated_string = "#_)"+mutated_string



        if self.read_check_already_string(mutated_string):
            mutated_string = self.generate_random_string(length)


        return mutated_string

    def save_success_input(self, count, error):
        with open(self.success_file, "a") as myfile:
            myfile.write(self.input + "\n")

    def save_detected_error(self, error):
        with open(self.error_file, "a") as myfile:
            myfile.write(error + "\n")


class CreateInput(InputReader):

    def __init__(self, given_input, generate=False):
        self.given_input = given_input
        self.success_file = "output/create.txt"
        self.error_file = "output/error.txt"
        if generate:
            self.method_name = self.generate_random_string_with_success(30)
            self.file_name = "md5.py"
        else:
            self.file_name, self.method_name = self.extract_input()

    def minimum_no_of_error(self):
        return 0

    def minimum_no_of_logs(self):
        return 20

    def extract_input(self):
        array = self.given_input.split(',')
        return array[0], array[1]

    def command(self):
        my_array = ["wsk", "action", "create", self.method_name, self.file_name, "--docker","pandeymanish93/python3action:serverless-cache"]
        my_string = ' '.join(my_array)
        print(my_string)
        return my_array

    def process(self):
        pass

    def compile_result(self, result):
        json_data = json.loads(result)
        return True

    def generate_random_string(self, length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def read_check_already_string(self, gen_str):
        # file success.txt file and get all string as array and check if the gen_str is already in the array
        data = []

        with open(self.success_file) as f:
            temp = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            data = [x.strip() for x in temp]

        if gen_str in data:
            return True
        else:
            return False

    def generate_random_string_with_success(self, length):
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

        if not self.read_check_already_string(mutated_string):
            return self.generate_random_string(length)

        return mutated_string

    def save_success_input(self):
        with open(self.success_file, "a") as myfile:
            myfile.write(self.input + "\n")

    def save_detected_error(self, error):
        with open(self.error_file, "a") as myfile:
            myfile.write(error + "\n")


class ActivationInput(InputReader):
    def __init__(self, activation_id):
        self.activation_id = activation_id

    def command(self):
        return ["wsk", "activation", "get", self.activation_id]

    def list_command(self):
        return ["wsk", "activation", "list"]

    def process(self):
        pass


class InputFactory:
    def create_input(self, method_type, *args):
        if method_type == "invoke":
            return InvokeInput(*args)
        elif method_type == "create":
            return CreateInput(*args)
        elif method_type == "activation":
            return ActivationInput(*args)
