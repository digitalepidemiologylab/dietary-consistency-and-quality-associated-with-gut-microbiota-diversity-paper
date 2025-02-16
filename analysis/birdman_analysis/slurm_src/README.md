# SLURM Execution Scripts

This directory contains scripts for preprocessing data and running BIRDMan analysis on a SLURM cluster.

## Files

### `filter_biom_and_metadata.py`

Preprocesses the BIOM table and metadata before BIRDMan_cli execution.

```python
import biom
import pandas as pd

# Input files
biom_path = "data/feature-table.biom" ## Modify this path to the BIOM table
metadata_path = "data/fay_meta_diets.csv" ## Modify this path to the metadata file

# Output files
filtered_biom = "data/table-filt.biom" ## Modify this path to the filtered BIOM table
filtered_metadata = "data/metadata-filt.tsv" ## Modify this path to the filtered metadata file
```

#### Functionality
1. Loads BIOM table and metadata
2. Filters features based on prevalence:
   - Keeps features present in at least 25% of samples
3. Matches samples between BIOM table and metadata and saves filtered data

### `submit_jobs_sequentially.sh`

Bash script for submitting sequential BIRDMan analysis jobs to SLURM.

```bash
./submit_jobs_sequentially.sh <variables_file>
```

#### Parameters
- `variables_file`: Text file containing list of variables to analyze (one per line)

#### Job Configuration
- Memory: 8GB
- CPUs: 4
- Time limits:
  - Run jobs: 6 hours
  - Summarize jobs: 1 hour

#### Workflow
1. For each variable in the input file:
   - Submits BIRDMan run job:
     ```bash
     birdman-cli run -i ./data/table-filt.biom \
                     -o ./outputs/$VARIABLE_NAME \
                     -m ./data/metadata-filt.tsv \
                     -f '$VARIABLE_NAME'
     ```
   - After run completion, submits summarize job:
     ```bash
     birdman-cli summarize -i outputs/$VARIABLE_NAME
     ```
   - Cleans up temporary directories after summarization:
     - inferences/
     - tmp/
     - logs/
     - slurm_out/

#### Dependencies
- Jobs are executed sequentially using SLURM dependencies
- Each summarize job depends on its corresponding run job
- Subsequent variable analysis starts after previous summarize job completes

## Usage

1. First, preprocess the data:
```bash
python filter_biom_and_metadata.py
```

2. Create a variables file (e.g., `variables.txt`) containing the variables to analyze:
```
fiber_eaten
protein_eaten
carb_eaten
...
```

3. Submit the SLURM jobs:
```bash
bash submit_jobs_sequentially.sh variables.txt
```

4. Monitor job progress using SLURM commands:
```bash
squeue -u $USER
sacct -u $USER
```

## Output Structure

For each variable, creates directory structure:
```
outputs/
└── variable_name/
    └── results/
        ├── beta_var.tsv
        └── differential_taxa.tsv
```

## Notes
- The script processes one variable at a time to manage computational resources
- Temporary files are automatically cleaned up after successful summarization
