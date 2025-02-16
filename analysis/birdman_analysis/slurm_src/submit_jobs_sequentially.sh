#!/bin/bash

# Check if the variables file is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <variables_file>"
  exit 1
fi

# Read the variables file
variables_file=$1

# Initialize the first job dependency as empty
previous_job_id=""

# Loop through each variable in the file
while IFS= read -r VARIABLE_NAME; do
  # Check if the variable is not empty
  if [ ! -z "$VARIABLE_NAME" ]; then
    echo "Submitting jobs for variable: $VARIABLE_NAME"

    # Submit the first job and capture the job ID
    if [ -z "$previous_job_id" ]; then
      # Submit the first job without dependency
      job_id1=$(birdman-cli run -i ./data/table-filt.biom -o ./outputs/$VARIABLE_NAME -m ./data/metadata-filt.tsv -f "$VARIABLE_NAME" -e rohan.singh@epfl.ch | grep -oP '\d+')
    else
      # Submit the first job with dependency on the previous job
      job_id1=$(sbatch --dependency=afterok:$previous_job_id --wrap="birdman-cli run -i ./data/table-filt.biom -o ./outputs/$VARIABLE_NAME -m ./data/metadata-filt.tsv -f '$VARIABLE_NAME' -e rohan.singh@epfl.ch" | grep -oP '\d+')
    fi

    # Submit the second job with dependency on the first job
    job_id2=$(sbatch --dependency=afterok:$job_id1 --wrap="birdman-cli summarize -i outputs/$VARIABLE_NAME; rm -r outputs/$VARIABLE_NAME/inferences/; rm -r outputs/$VARIABLE_NAME/tmp/; rm -r outputs/$VARIABLE_NAME/logs/; rm -r outputs/$VARIABLE_NAME/slurm_out/" | grep -oP '\d+')

    # Update the previous job ID for the next iteration
    previous_job_id=$job_id2
  fi
done < "$variables_file"

echo "All jobs have been submitted sequentially."


