#!/bin/bash

# Set a default value for the parameter
default_value="update"

# Check if a parameter was passed and set the variable accordingly
if [[ -n "$1" ]]; then
  parameter="$1"
else
  parameter="$default_value"
fi

# Perform the if/else if conditions based on the value of the parameter
if [[ "$parameter" == "delete" ]]; then

    wsk -i action delete md5

elif [[ "$parameter" == "create" ]]; then
    wsk -i action create all_combination all_combinations.py --kind python:3 --memory 96

elif [[ "$parameter" == "update" ]]; then

    wsk -i action update md5 md5.py --kind python:3

elif [[ "$parameter" == "local" ]]; then

    wsk action update md5 md5.py --kind python:3

fi





