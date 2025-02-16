# Gut Diversity Analysis

This repository contains analysis scripts for investigating relationships between dietary patterns, lifestyle factors, and gut microbiome diversity.

## Project Structure

```
gut_diversity_analysis/
├── config/
│   └── variables.py         # Configuration variables and parameters
├── utils/
│   └── data_processing.py   # Utility functions for data processing
├── analysis notebooks/
│   ├── diversity_correlations.ipynb    # Correlation analysis between variables and diversity metrics
│   ├── evident_effect_sizes.ipynb      # Effect size analysis of categorical variables
│   ├── explained_variance.ipynb        # Variance decomposition analysis
│   └── upset_plot.ipynb                # Dietary pattern intersection analysis
├── effects_model_diversity_HEI_Age.R   # Linear modeling of HEI, age, and gender effects on diversity
└── pcoa_and_boxplots.R                # PCoA visualization and statistical boxplot analysis
```

## Analysis Components

### 1. Diversity Correlations
- Examines Spearman correlations between:
  - Dietary indices
  - Nutrient intake
  - Food group consumption
  - Personal characteristics
  - Coefficient of variation metrics
- Visualizes relationships with α-diversity (Shannon index)
- Includes heatmap visualization of microbial diversity correlations
- Features radar plot analysis comparing dietary patterns:
  - Contrasts food group consumption between HEI quartiles (Q1 vs Q4)
  - Visualizes eight key dietary categories:
    - Vegetables, Fruits, Grains/potatoes/pulses, Meat, Sweets/snacks/alcohol, Fast food, Bread, Coffee
  - Categories arranged by ascending median difference between quartiles

### 2. Factor Effect Size Analysis
- Investigates the impact of categorical variables on three alpha diversity metrics:
  - Observed Features (species richness)
  - Shannon Entropy (richness and evenness)
  - Faith's Phylogenetic Diversity (PD)
- Calculates effect sizes using:
  - Cohen's d for binary variables
  - Cohen's f for multi-level categorical variables
- Includes pairwise analysis between extreme groups (e.g., Q1 vs Q4 quartiles)
- Analyzes beta diversity using unweighted UniFrac distances
- Limited to categorical variables with ≤6 levels

### 3. Explained Variance Analysis
- Quantifies the proportion of α-diversity variance explained by different feature sets:
  - All features combined
  - Personal characteristics
  - Nutritional factors (combined and separate):
    - Macronutrients
    - Micronutrients
    - Diet indices
    - Food groups
- Uses linear regression to calculate R² values
- Visualizes relative contributions through a bar plot
- Enables comparison of feature set importance in predicting gut diversity

### 4. Combinatorial Effects Modeling
- Linear modeling of Shannon diversity relationships with:
  - HEI (Healthy Eating Index)
  - Age groups (<35, 35-50, >50)
  - Gender
  - BMI categories
  - Other lifestyle factors
- Includes interaction analysis between key variables
- Visualization of predicted relationships and effect modifications

### 5. Visualization Analysis
- PCoA plots of UniFrac distances with:
  - HEI quartile overlay
  - Statistical ellipses
- Statistical boxplot analysis of diversity metrics across:
  - Age groups
  - Smoking status
  - BMI categories

### 6. Dietary Pattern Analysis (Upset Plot)
Visualizes intersections of dietary patterns focusing on:
- Vegetable/Fruit consumption
- Fiber intake
- Fast food consumption
- Meat consumption

Additional metrics plotted for each intersection:
- HEI, Shannon diversity, Age, BMI

## Dependencies
- Python libraries: Pandas, NumPy, Matplotlib, Seaborn, Upsetplot, QIIME2 (for UniFrac analysis)
- R libraries: ggplot2, dplyr, forcats, patchwork, ape, ggstatsplot, ggsignif, sjPlot

## Usage
1. Ensure all dependencies are installed
2. Configure variables in `config/variables.py`
3. Run notebooks and R scripts for respective analyses

## Notes
- UniFrac distance matrix must be unzipped before running beta diversity analysis
- Plots are automatically saved to `../../figures/gut_diversity_analysis/` directory