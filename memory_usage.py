import os
import glob

def get_recently_updated_file(directory,name):
    file_pattern = os.path.join(directory, 'wsk*'+name+'.txt')
    files = glob.glob(file_pattern)
    if files:
        most_recent_file = max(files, key=os.path.getmtime)
        return most_recent_file
    else:
        return None

def get_last_value_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            last_value = ''.join(filter(str.isdigit, last_line))
            if last_value:
                return int(last_value)
            return last_line
        else:
            return None


def get_memory_detail(name):
    directory = "data/memory"

    recent_file = get_recently_updated_file(directory,name)

    return get_last_value_from_file(recent_file),recent_file.replace("data/memory/", "")


get_memory_detail("md5")