# CV Mean Validation Analysis

This analysis examines the relationship between coefficient of variation (CV) in fruit consumption, total fruit consumption, and dietary diversity (Shannon entropy). This is to demonstrate decrease in shannon entropy with increase in CV of fruit consumption.

## Contents

- `cv_mean_validation.ipynb`: Jupyter notebook containing the analysis code and visualizations

## Analysis Overview

The analysis explores several key relationships:

1. **Relationship between CV Fruits and Total Fruit Consumption**
   - Scatter plot visualization of CV Fruits vs total fruits eaten
   - Points colored by Shannon entropy (dietary diversity)
   - Reference lines at 175g and 200g fruit consumption as an example window size

2. **Example Window size of 175-200g Fruit Consumption Range**
   - Analysis on a data split of subjects eating 175-200g fruits daily
   - From this subset, data is split into CV quintiles and colored by Shannon entropy
   - highlights CV quintile boundaries

3. **Systematic Analysis Across Fruit Consumption Ranges**
   - Each plot shows how Shannon entropy varies with CV across different fruit consumption levels (25g intervals)
   - Shows whether high CV is associated with above/below average dietary diversity

4. **Reverse Analysis: CV Ranges vs Fruit Consumption Quintiles**
   - Reverse perspective examining fixed CV ranges
   - Shows distribution of Shannon entropy across fruit consumption quintiles

## Key Findings

- When examining subjects with similar average fruit consumption, dietary diversity (Shannon entropy) tends to decrease with increasing CV in ~75% of the analyzed windows
- This relationship is not evident when examining fixed CV ranges across different levels of fruit consumption

## Generated Figures

Generates several visualization files in figures folder (root directory):
- `cv_fruits_vs_fruits_eaten.png`: Initial scatter plot analysis
- `cv_fruits_vs_fruits_eaten_175_200g.png`: Focused analysis of 175-200g consumption range
- `cv_fruits_quintiles_mean_validation.png`: Comprehensive multi-panel analysis
- `cv_fruits_quintiles_mean_validation_reverse.png`: Reverse analysis visualization
