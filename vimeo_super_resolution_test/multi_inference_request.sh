#!/bin/bash

# Set the base URL
BASE_URL="http://localhost:8080/predictions"

# Define the models
MODELS=("swinIR")

# Define the input and target directories
INPUT_DIR="low_resolution"
OUTPUT_DIR="results"

# Loop over the models
for MODEL in "${MODELS[@]}"; do
    # Loop over all the sequences in the input directory
    for SEQ in "${INPUT_DIR}"/*/*; do
        # Get the sequence name
        SEQ_NAME="$(basename "${SEQ}")"

        # Get the parent directory name
        PARENT_DIR="$(basename "$(dirname "${SEQ}")")"

        # Loop over all the input files in the sequence
        for INPUT_FILE in "${SEQ}"/*im4.png; do
            # Get the input file name
            INPUT_FILE_NAME="$(basename "${INPUT_FILE}")"

            # Define the output file name
            OUTPUT_FILE="${OUTPUT_DIR}/${PARENT_DIR}/${SEQ_NAME}/${INPUT_FILE_NAME%.*}_${MODEL}.png"
            
            # Create the output directory if it doesn't exist
            mkdir -p "$(dirname "${OUTPUT_FILE}")"

            # Call the inference API for the current model and input file
            curl "${BASE_URL}/${MODEL}" -T "${INPUT_FILE}" -o "${OUTPUT_FILE}"
        done
    done
done
# Wait for all the requests to finish
wait
