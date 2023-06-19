import subprocess
import json
import random
import string
import time
import os
import sqlalchemy as db
from sqlalchemy import create_engine
from memory_usage import get_memory_detail
import re
from container_memory import get_container_memory

engine = create_engine(f'sqlite:////Users/manish/projects/serverless/fuzzerapplication/loganalysis.db',
                       connect_args={'check_same_thread': False})



def list_the_latest_transaction_id():
    # execute a raw SQL query
    result = engine.execute("SELECT * FROM log WHERE NOT transaction_id LIKE '#tid_sid%' ORDER BY id DESC LIMIT 1;")
    for row in result:
        return row['transaction_id']


def count_number_of_rows(transaction_id):
    # execute a raw SQL query
    result = engine.execute("SELECT COUNT(*) FROM log WHERE transaction_id = '" + transaction_id + "'")

    for row in result:
        return row['COUNT(*)']


def refresh_function(memory,create_file_name):
    if memory > 0:
        cmd = ["wsk","action","update","md5",create_file_name,"--memory",str(memory)]
    else:
        cmd = ["wsk", "action", "update", "md5", create_file_name]
    execute_command_with_retry(cmd)


def count_number_of_rows_with_error(transaction_id):
    # execute a raw SQL query
    result = engine.execute(
        "SELECT COUNT(*) FROM log WHERE transaction_id = '" + transaction_id + "' AND loglevel = 'ERROR'")

    for row in result:
        return row['COUNT(*)']


def extract_container_from_transaction_id(transaction_id):
    # execute a raw SQL query
    result = engine.execute(
        "SELECT message FROM log WHERE transaction_id = '" + transaction_id + "' AND message LIKE 'sending arguments to%' ORDER BY id DESC")
    output = ""
    for row in result:
        output = row['message']
    result = re.search(r'ContainerId\((.*?)\)', output)
    if result:
        container_id = result.group(1)
        return container_id
    return None

from inputbuilder import InputFactory


def list_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


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


def fuzzing_loop():
    start_time = time.time()
    duration = 1000  # 5 seconds

    # Example usage
    directory = "input"  # Replace with the directory path you want to list files from
    files = list_files(directory)
    times = 20

    for file in files:
        # read the txt file
        factory = InputFactory()
        # Open the file in read mode
        with open(file, "r") as fc:
            # Iterate over each line in the file
            file_name = os.path.basename(file)
            file_name_only = os.path.splitext(file_name)[0]
            create_file_name = 'md5.py'
            refresh_function(0,create_file_name)

            for line in fc:
                memory = 256
                # Process each line (e.g., print it)
                fc = factory.create_input(file_name_only, line.strip(), False)
                cmd = fc.command()

                result = execute_command_with_retry(cmd)

                transaction_id = list_the_latest_transaction_id()
                count = count_number_of_rows(transaction_id)
                error = count_number_of_rows_with_error(transaction_id)

                #container_id = extract_container_from_transaction_id(transaction_id)
                memory_used,docker_name = get_container_memory()


                # memory_used,docker_name = get_memory_detail(fc.method_name)
                fc.write_output_message(count, error, memory_used,docker_name,memory,create_file_name)

                if count > fc.minimum_no_of_logs() and error <= fc.minimum_no_of_error():
                    print("Mutation required")
                else:
                    transaction_id_save = transaction_id+","+str(count)+","+str(error)
                    fc.save_detected_error(transaction_id_save)


            while time.time() - start_time < duration:
                fc = factory.create_input(file_name_only, "generate", True)
                memory = fc.get_updated_memory()
                create_file_name = fc.get_create_file_name()
                refresh_function(memory,create_file_name)


                cmd = fc.command()
                result = execute_command_with_retry(cmd)
                compile_result = fc.compile_result(result)

                transaction_id = list_the_latest_transaction_id()
                count = count_number_of_rows(transaction_id)
                error = count_number_of_rows_with_error(transaction_id)
                #memory_used,docker_name = get_memory_detail(fc.method_name)
                #memory_used, docker_name = get_container_memory(container_id)
                memory_used, docker_name = get_container_memory()
                fc.write_output_message(count, error, memory_used,docker_name,memory,create_file_name)


                #

                if count > fc.minimum_no_of_logs() and error <= fc.minimum_no_of_error():
                    fc.save_success_input(count,error)

                else:
                    transaction_id_save = transaction_id + "," + str(count) + "," + str(error)
                    fc.save_detected_error(transaction_id_save)

                time.sleep(2)




if __name__ == "__main__":
    # Start the fuzzing loop
    fuzzing_loop()
