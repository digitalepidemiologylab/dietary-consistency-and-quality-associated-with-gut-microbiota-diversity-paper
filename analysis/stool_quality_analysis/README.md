# Stool Quality Analysis

This directory contains code for analyzing relationships between stool quality, dietary factors, and microbiome data.

## Directory Structure
```
.
├── prep_stool_quality_meta.ipynb
└── utils/
    ├── __pycache__/
    │   └── data_processing.cpython-38.pyc
    └── data_processing.py
```

## Key Files

### prep_stool_quality_meta.ipynb
Main analysis notebook that:
- Processes stool quality survey data
- Filters users based on minimum response requirements (≥5 days)
- Calculates stool quality proportions per user
- Identifies users with predominantly great, constipated, or diarrhea stool quality
- Analyzes correlations between metadata features and stool quality
- Generates Figure 5 for the manuscript, including:
  - Correlations to great stool quality proportion
  - Correlations to diarrhea proportion
  - Boxplots of relationships with HEI, Shannon entropy, and dietary components
  - HEI quartile distribution across stool quality groups
  - Partial correlations between microbes and diarrhea


## Data Dependencies
The analysis requires the following input files (located in `../../data/`):
- `fay_meta_diets.csv`: Metadata and dietary information
- `fay_eve_survey_may24.csv`: Evening survey responses containing stool quality data
- `partial_correlations_microbe_to_diarrhea.csv`: Microbiome correlation data generated from partial correlation analysis

### Generating Partial Correlations Data
Before running this notebook, you need to generate the partial correlations data:

1. Navigate to the `taxa_correlations` directory
2. Run `run_partial_correlations_stool_quality_analysis.ipynb`
3. This will generate `partial_correlations_microbe_to_diarrhea.csv` in the `../../data/` directory
4. Once generated, this CSV file will be used by `prep_stool_quality_meta.ipynb` for visualization in Figure 5 (particularly Panel I)

## Output
- Generates Figure 5 for the manuscript (`../../figures/stool_quality_analysis/Figure_5.png`)
- Saves processed metadata to `../../data/stool_quality_meta.csv`

## Dependencies
- Python libraries: pandas, numpy, matplotlib, seaborn

## Usage
1. Ensure all required data files are present in the `../../data/` directory
2. Run `prep_stool_quality_meta.ipynb` to perform the analysis and generate figures

## Figure Components
Figure 5 consists of multiple panels showing:
- Panels A-B: Feature correlations with stool quality metrics
- Panels C-E: Boxplots showing relationships with dietary indices
- Panels F-H: HEI quartile distributions
- Panel I: Microbe-diarrhea partial correlations heatmap