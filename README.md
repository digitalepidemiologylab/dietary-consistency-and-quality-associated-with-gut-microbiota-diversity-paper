# Dietary Consistency and Quality Associated with Gut Microbiota Diversity

This repository contains analysis code and data for investigating associations between dietary patterns, consistency, and gut microbiota diversity using detailed temporal nutrition data from the "Food & You" digital cohort (2019-2022) conducted in Switzerland with 1000+ participants.

## Repository Structure

```
.
├── analysis/
│   ├── gut_diversity_analysis/     # Core diversity metrics and correlations
│   ├── taxa_correlation_analysis/  # Taxonomic correlation studies
│   ├── birdman_analysis/          # Differential abundance analysis
│   ├── ml_analysis/               # Machine learning predictions
│   ├── stool_quality_analysis/    # Stool quality associations
│   └── cv_mean_validation/        # Dietary consistency validation
├── data/                          # Input data files
├── figures/                       # Manuscript figures
├── qiime/                         # QIIME2 outputs
└── results/                       # Analysis results
```

## Analysis Components

### [Gut Diversity Analysis](analysis/gut_diversity_analysis/)
- Investigates relationships between dietary patterns and microbiome diversity
- Includes correlation analysis, effect sizes, and variance decomposition

### [Taxa Correlation Analysis](analysis/taxa_correlation_analysis/)
- Examines correlations between differentially abundant taxa and dietary variables
- Includes both dietary and stool quality correlation analyses

### [BIRDMan Analysis](analysis/birdman_analysis/)
- Differential abundance analysis using Bayesian inference
- Identifies key microbial associations with dietary variables

### [Machine Learning Analysis](analysis/ml_analysis/)
- Predicts dietary indices from microbiome composition and vice versa
- Includes feature importance analysis and performance evaluation

### [Stool Quality Analysis](analysis/stool_quality_analysis/)
- Links dietary patterns and microbiome composition to stool quality metrics
- Focuses on relationships with HEI and dietary components

### [CV Mean Validation](analysis/cv_mean_validation/)
- Validates dietary consistency metrics
- Examines relationships with diversity measures

## Dependencies

1. Python: pandas, numpy, scipy, scikit-learn, xgboost, matplotlib, seaborn, scikit-bio, BIRDMan_cli, pingouin
2. R: ggplot2, dplyr, patchwork, ape, ggstatsplot

## Usage
Please refer to individual directories for detailed documentation.

## Data Files
- Microbiome data: QIIME2 outputs in `qiime/`
- Metadata in `data/`
- Manuscript figures in `figures/`