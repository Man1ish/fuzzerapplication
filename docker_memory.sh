#!/bin/bash

if [ ! -d "data/memory" ]; then
  mkdir -p data/memory
fi

if [ ! -d "data/functions" ]; then
  mkdir -p data/functions
fi

while true; do
    # Get memory usage of all containers
    docker stats --all --format "{{.Name}} {{.MemUsage}}" | while read -r line; do
        # Get container name
        container_name=$(echo $line | awk '{print $1}')

        # Check if container name starts with wsk
        if [[ $container_name == wsk* ]]; then
            # Current timestamp
            timestamp=$(date +"%Y-%m-%d %T")
            # Get memory usage
            mem_usage=$(echo $line | awk '{print $2}')

            # Write memory usage to file
            if [[ -n $mem_usage && $mem_usage != "--" ]]; then
                echo $mem_usage > "data/memory/$container_name.txt"
            else
                echo "" > "data/memory/$container_name.txt"
            fi
        fi
    done
    sleep 0.3
done
