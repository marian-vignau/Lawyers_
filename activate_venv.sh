#!/bin/bash

# Check if the virtual environment is already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Virtual environment is not active. Please activate it before running this command."
    exit 1
else
    echo "Virtual environment is active."
fi


