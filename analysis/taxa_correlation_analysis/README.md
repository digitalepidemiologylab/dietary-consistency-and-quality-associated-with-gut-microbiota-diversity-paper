# Taxa Correlation Analysis

This directory contains utilities and scripts for analyzing and visualizing taxonomic correlations in microbiome data. The code specifically supports the creation of two visualization types:

1. Radial plots showing relationships between microbial abundance and various metadata variables
2. Taxa correlation heatmaps displaying spanning multiple taxa (from BIRDMan) and dietary features

## Directory Structure

```
.
├── run_taxa_correlations_and_plot.ipynb  # Main notebook for running analyses
└── utils/                                # Utility functions
    ├── data_processing.py               # Data processing and transformation functions
    └── plotting_functions.py            # Visualization and plotting utilities
```

## Core Components

### Data Processing (`utils/data_processing.py`)

Key functionalities:
- Loading and processing prevalence data for ASVs
- Transforming count data using CLR (Centered Log-Ratio) or relative abundance methods
- Filtering microbes based on prevalence thresholds
- Creating data quartiles for analysis
- Processing taxonomic names and strings
- Summarizing microbe-food variable relationships
- Extracting and formatting taxonomy information at different levels (species, genus, family, etc.)

### Plotting Functions (`utils/plotting_functions.py`)

Implements visualization functions for:
- Creating polar plots for individual taxa correlations
- Generating complex heatmaps with taxonomic annotations
- Handling partial correlations and statistical significance (FDR-adjusted p-values)
- Managing color schemes for different taxonomic levels
- Creating custom legends and annotations for both plot types
- Supporting hierarchical clustering visualization

### Main Notebook

The `run_taxa_correlations_and_plot.ipynb` notebook implements the following pipeline:

1. Data Loading and Processing:
   - Loads metadata and count data
   - Applies CLR transformation on count data
   - Filters microbes based on prevalence (threshold = 0.05) 
   - Saves prevalence to root data folder

2. Correlation Analysis:
   - Performs partial correlations adjusting for age and BMI
   - Processes significant taxa from Birdman analysis
   - Analyzes relationships with dietary variables

3. Visualization:
   - Creates a combined figure with 4 panels:
     - Panel A: Correlation heatmap
     - Panels B-D: Radial plots for specific taxa

4. Saves the final figure to `../../figures/taxa_correlation_analysis/Fig3.png`

## Usage

To use this analysis pipeline:

1. Ensure your data follows the expected structure:
   - ASV count data: `../../qiime/table_rarefied.tsv`
   - Taxonomy data (one of):
     - `../../qiime/taxonomy_rarefied-table_2022_10/taxonomy.tsv`
     - `../../qiime/taxonomy_rarefied-table_2024_09/taxonomy.tsv`
   - Metadata: `../../data/fay_meta_diets.csv`
   - Birdman analysis results in `../birdman_analysis/outputs/`

2. Run the Jupyter notebook `run_taxa_correlations_and_plot.ipynb`

3. The resulting figure will be saved as `Fig3.png` in `../../figures/taxa_correlation_analysis/`

## Dependencies

Required Python packages:
- pandas, numpy, matplotlib, seaborn, scikit-bio (for CLR transformation) 
- pingouin (for partial correlations), statsmodels, tqdm (for progress bars)

## Output Visualizations

The pipeline generates a combined figure with multiple panels:

1. **Correlation Heatmap (Panel A)**:
   - Shows correlations between taxa and dietary variables
   - Includes statistical significance annotations (* q<0.05, ** q<0.01, *** q<0.001)
   - Features hierarchical clustering
   - Color-coded by taxonomic order

2. **Radial Plots (Panels B-D)**:
   - Individual plots for selected taxa
   - Shows relationship with 10 key dietary variables
   - Bars indicate Q4 (highest quartile) median values
   - Dots show Q1 (lowest quartile) median values
   - Color-coded by correlation strength using PiYG color scheme
   - Includes prevalence percentage in the center