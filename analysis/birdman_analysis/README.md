# Diet-Microbiome Association Analysis using BIRDMan

This repository contains the analysis pipeline and results for investigating diet-microbiome associations using BIRDMan (Bayesian Inference of Regression for Differential Microbiome Analysis). BIRDMan is a framework for performing differential abundance analyses of microbiome data, implemented as a Python interface to the Stan probabilistic programming language. For implementation details and CLI usage, please refer to the [BIRDMAn-CLI repository](https://github.com/lucaspatel/BIRDMAn-CLI/tree/develop).

## Repository Structure

```
.
├── Supplementary_File_1.tsv          # Combined differential abundance results
├── extract_differential_taxa.ipynb    # Notebook for extracting differential taxa
├── generate_supplementary_file_1.py   # Script to generate supplementary file
├── outputs/                          # Results organized by nutritional variables
│   ├── [variable_name]/              # One directory per nutritional variable
│   │   └── results/
│   │       ├── beta_var.tsv          # BIRDMan regression results
│   │       └── differential_taxa.tsv  # Differential abundance results
├── slurm_src/                        # SLURM submission scripts
└── topn_plots/                       # Visualization of beta variance results
```

## Analysis Pipeline

1. **SLURM Execution (slurm_src/)**
   - Contains scripts for running BIRDMan analysis on a SLURM cluster
   - Processes each nutritional variable independently

2. **BIRDMan Analysis (outputs/)**
   - Contains differential abundance results for various nutritional variables generated from BIRDMan_cli

3. **Differential Taxa Analysis (extract_differential_taxa.ipynb)**
   - Processes BIRDMan results and generates comprehensive visualizations
   - Key analyses include:
     - Log ratio (LR) calculations and correlations
     - Mirror plots showing numerator vs denominator ASV counts
     - Correlation analysis between different nutritional variables
     - Bipartite network visualization of microbe-feature relationships
   - Required input files:
     - Partial correlation data (data/partial_corr_across_feats.csv)
     - Taxonomy mappings (qiime/taxonomy_rarefied-table_2024_09/taxonomy.tsv)
     - Metadata (data/fay_meta_diets.csv)
     - Rarefied table (qiime/table_rarefied.tsv)
     - Microbe prevalence data (data/prevalence_microbes.csv)
   - Generates multiple visualization outputs:
     - Differential abundance counts (figures/birdman_analysis/diff_abun_counts.png)
     - LR correlations (figures/birdman_analysis/log_ratio_HEI_fast_food.png)
     - LR-Foods heatmap (figures/birdman_analysis/diff_abun_clustermap.png)
     - Network plots (figures/birdman_analysis/network_class_level.png)

## File Descriptions

### Output Files

- **beta_var.tsv**: Contains BIRDMan regression results including:
  - Intercept means and standard deviations
  - Variable-specific coefficients
  - HDI (Highest Density Interval) values
- **differential_taxa.tsv**: Contains differential abundance results (within credible interval)

### Results Location
- Plots are saved in "figures/birdman_analysis" of the root directory
- Top 25 differential taxa for each variable are saved in "topn_plots"

## Dependencies
Required Python packages: BIRDMan_cli, numpy, pandas, matplotlib, seaborn, networkx, scipy, adjustText

## Usage

1. **Preprocess Data**
   ```bash
   cd slurm_src
   python filter_biom_and_metadata.py
   ```

2. **Run BIRDMan Analysis**
   ```bash
   # Create a variables.txt file with variables to analyze
   bash submit_jobs_sequentially.sh variables.txt
   ```

3. **Generate Visualizations**
   - Run the Jupyter notebook:
   ```bash
   jupyter notebook extract_differential_taxa.ipynb
   ```

For detailed SLURM execution instructions, see the README in the `slurm_src` directory.