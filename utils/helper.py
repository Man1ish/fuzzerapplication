import re
import json

class TemplateChecker:
    def __init__(self, log_template, log_string):
        self.log_template = log_template
        self.log_string = log_string
        self.variables = self.extract_variable()
        self.result = self.calculate_data()

    def extract_variable(self):
        pattern = r"\{(.*?)\}"
        matches = re.findall(pattern, self.log_template)
        return matches

    def calculate_data(self):
        result = {}
        log_template_array = self.log_template.split()
        log_string_array = self.log_string.split()

        for log_template, log_string in zip(log_template_array, log_string_array):
            for variable in self.variables:
                if variable in log_template:
                    start, end = self.extract_position(log_template)
                    if not start or not end:
                        continue
                    value = self.extract_pattern(log_string, start, end)
                    result[variable] = value

        return result

    def extract_position(self, str_val):
        start_index = str_val.rfind('{') - 1
        end_index = str_val.rfind('}') + 1

        if start_index >= 0 and end_index < len(str_val):
            return str_val[start_index], str_val[end_index]
        else:
            return None, None

    def extract_pattern(self, str_val, first, second):
        start_index = str_val.rfind(first) + 1
        end_index = str_val.rfind(second)




        val = str_val[start_index:end_index]

        if val == '' or val == ' ':
            start_index = str_val.find(first)
            if start_index == -1:
                pass
            end_index = str_val.find(second, start_index + 1)
            if end_index == -1:
                return None  # No closing quote found
            extracted_text = str_val[start_index + 1: end_index]
            return extracted_text

        return val

def read_config_file(filename='config.json'):
    with open(filename, 'r') as file:
        config = json.load(file)

    return config

