# Taxa Correlation Analysis

This directory contains utilities and scripts for analyzing and visualizing taxonomic correlations in microbiome data. The code supports multiple types of analyses:

1. Diet-Microbiome Correlations:
   - Radial plots showing relationships between microbial abundance and various metadata variables
   - Taxa correlation heatmaps displaying spanning multiple taxa (from BIRDMan) and dietary features
   - Forms Figure 3 in the paper

2. Stool Quality Analysis:
   - Partial correlations between microbiome composition and stool quality metrics
   - Focus on diarrhea proportion analysis

## Directory Structure

```
.
├── run_taxa_correlations_and_plot.ipynb     # Main notebook for dietary analysis
├── run_taxa_correlations_stool_quality.ipynb # Notebook for stool quality analysis
└── utils/                                   # Utility functions
    ├── data_processing.py                  # Data processing and transformation functions
    └── plotting_functions.py               # Visualization and plotting utilities
```

## Core Components

### Data Processing (`utils/data_processing.py`)

Key functionalities:
- Loading and processing prevalence data for ASVs
- Transforming count data using CLR (Centered Log-Ratio) or relative abundance methods
- Filtering microbes based on prevalence thresholds
- Creating data quartiles for analysis
- Processing taxonomic names and strings
- Summarizing microbe-variable relationships
- Extracting and formatting taxonomy information at different levels (species, genus, family, etc.)

### Plotting Functions (`utils/plotting_functions.py`)

Implements visualization functions for:
- Creating polar plots for individual taxa correlations
- Generating complex heatmaps with taxonomic annotations
- Handling partial correlations and statistical significance (FDR-adjusted p-values)
- Managing color schemes for different taxonomic levels
- Creating custom legends and annotations
- Supporting hierarchical clustering visualization

### Analysis Notebooks

#### Dietary Analysis (`run_taxa_correlations_and_plot.ipynb`)

Implements the following pipeline:

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

#### Stool Quality Analysis (`run_taxa_correlations_stool_quality.ipynb`)

Performs analysis of microbiome associations with stool quality:

1. Data Processing:
   - Loads and transforms stool quality data
   - Processes taxonomy

2. Analysis:
   - Calculates correlations with diarrhea
   - Controls for age and BMI

3. Output:
   - Saves results to `../../data/partial_correlations_microbe_to_diarrhea.csv`

## Usage

1. The data should follow this structure:
   - ASV count data: `../../qiime/table_rarefied.tsv`
   - Taxonomy data (one of):
     - `../../qiime/taxonomy_rarefied-table_2022_10/taxonomy.tsv`
     - `../../qiime/taxonomy_rarefied-table_2024_09/taxonomy.tsv`
   - Metadata:
     - Dietary analysis: `../../data/fay_meta_diets.csv`
     - Stool quality analysis: `../../data/stool_quality_meta.csv`
   - Birdman analysis results in `../birdman_analysis/outputs/`

2. Run the desired analysis notebook:
   - For dietary correlations: `run_taxa_correlations_and_plot.ipynb`
   - For stool quality analysis: `run_taxa_correlations_stool_quality.ipynb`
   - After this, go to stool_quality_analysis folder for further analysis.

## Dependencies

Required Python packages:
- pandas, numpy, matplotlib, seaborn, scikit-bio (for CLR transformation)
- pingouin (for partial correlations), statsmodels, tqdm (for progress bars)

## Output Files

1. Dietary Analysis:
   - Combined figure (`Fig3.png`) in `../../figures/taxa_correlation_analysis/`
   - Contains correlation heatmap and radial plots

2. Stool Quality Analysis:
   - Partial correlations results in `../../data/partial_correlations_microbe_to_diarrhea.csv`
   - Includes correlation coefficients and taxonomic information for each ASV