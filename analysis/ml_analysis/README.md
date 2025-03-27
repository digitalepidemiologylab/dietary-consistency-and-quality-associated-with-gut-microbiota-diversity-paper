# Dietary Analysis ML Pipeline

This machine learning pipeline for dietary analysis includes classification and regression models to predict:
Objective 1: various nutritional metrics, dietary indices using microbiome data.
Objective 2: alpha diversity metrics using nutritional and anthropometric data.

## Project Structure

```
.
├── analysis.ipynb
├── config/
│   └── variables.py
├── graphlan_files/
│   ├── README.md
│   ├── generate_graphlan_plot.sh
│   ├── nutrition_features_annotations.txt
│   ├── nutrition_features_importance_plot.png
│   ├── nutrition_features_tree.txt
│   └── nutrition_features_tree_annotated.xml
├── results/
│   ├── Supplementary_File_2.xls
│   ├── classifier_performance_auroc.csv
│   ├── classifier_performance_diversity_auroc.csv
│   ├── clr_featImp.csv
│   ├── clr_featImp_diversity.csv
│   └── regressor_performance_full.csv
├── run_models.py
├── run_models_diversity.py
└── utils/
    ├── data_processing.py
    └── model_utils.py
```

## Main Scripts

### run_models.py
The primary script for running the Objective 1 of the ML analysis pipeline.
- Builds both classification and regression models (100 iterations for each variable)
- Outputs performance metrics and feature importance scores in the results directory
- Note: Runs for all variables in the config/variables.py file

### run_models_simple.py
A simplified version of the ML analysis pipeline for quicker testing and demonstration.
- Runs for only 1 target variable at a time

### run_models_diversity.py
For Objective 2 of the ML analysis pipeline.
- Focuses on diversity measures like Faith's PD, Shannon entropy, Pielou evenness and Observed Features
- Builds only classification models with multiple iterations (50)
- Outputs feature importance in the results directory

### analysis.ipynb
Jupyter notebook for visualizing and analyzing model outputs from both objectives.

## Configuration

The `config/variables.py` file defines variable groupings for the analysis, including macronutrients, micronutrients, food groups, dietary indices, and demographic variables.

## Results

Analysis results are stored in the `results/` directory:
- Classification performance metrics (AUROC) and feature importance for Objective 1
- Classification performance metrics (AUROC) and feature importance for Objective 2
- Regression performance metrics for Objective 1

## Visualization

The `graphlan_files/` directory contains files for generating GraPhlAn plot of feature importance for classifiers of Objective 1.

## Data Requirements

The pipeline expects the following input data files (not included in repository):
- `fay_meta_diets.csv`: Main metadata and dietary information
- `counts_data_with_taxonomy.csv`: Count data with taxonomic information

## Usage

To run the main analysis:
```bash
python run_models.py
```
Depending upon the number of variables you use, this will take a while to run (100 iterations for each variable). Hence run it on a server. The XGBoost models use all the cores for parallel processing.

To run the diversity prediction analysis:
```bash
python run_models_diversity.py
```

To visualize results, run the analysis.ipynb Jupyter notebook.

## Dependencies
pandas, numpy, scikit-learn, tqdm, xgboost, matplotlib, seaborn, scipy, graphlan