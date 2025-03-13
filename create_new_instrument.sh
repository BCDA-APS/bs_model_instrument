#!/usr/bin/env bash

# Check if instrument name was provided
if [ $# -eq 0 ]; then
    echo "Error: Instrument name is required"
    echo "Usage: $0 <instrument_name>"
    exit 1
fi

# Get the instrument name from the first argument
instrument_name=$1

# Call the create_new_instrument function
python3 -m bits.utils.create_new_instrument "${instrument_name}" "src/"