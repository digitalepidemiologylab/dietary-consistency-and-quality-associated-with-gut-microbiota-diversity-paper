"""Script to analyze diversity metrics using classification models."""

import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder

from utils.data_processing import create_quartiles
from utils.model_utils import train_and_evaluate_classifier
from config.variables import (
    NUTRI_MACRO_VARS,
    NUTRI_MICRO_VARS,
    NUTRI_CFG_VARS,
    NUTRI_FG_VARS,
    NUTRI_DI_VARS,
    AMOUNT_VARS,
    # PERSONAL_VARS,
    get_cv_vars,
)


def convert_to_numeric(df, cols):
    """
    Convert non-numeric columns in the dataframe to numeric using label encoding.

    Parameters:
    - df: pandas DataFrame
    - cols: list of column names to convert

    Returns:
    - DataFrame with converted columns
    """
    df = df.copy()
    for col in cols:
        if df[col].dtype == "object":
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
    return df


def process_string(s):
    """Process string to make it more readable/usable as a column name."""
    return s.replace(" ", "_").lower()


def analyze_diversity_metrics(meta, diversity_metrics, n_iterations=50):
    """
    Analyze diversity metrics using classification models.

    Parameters:
    - meta: pandas DataFrame containing metadata and features
    - diversity_metrics: list of diversity metrics to analyze
    - n_iterations: number of iterations for each analysis

    Returns:
    - tuple of (classification results, feature importance DataFrame)
    """
    diversity_clf_res = {}
    diversity_clf_auprc = {}
    diversity_clf_featImp = {}

    for col_target in diversity_metrics:
        print(f"\nAnalyzing {col_target}")

        # Prepare data
        v = meta.copy()
        v["hPDI_Quintile"] = v["hPDI_Quintile"].astype(int)
        v["PDI_Quintile"] = v["PDI_Quintile"].astype(int)

        # Define columns
        categ_cols_clf = ["gender", "swiss_citizen"]

        cv_vars = get_cv_vars(meta)  # Import this from config.variables

        PERSONAL_VARS = [
            "age",
            "bmi",
            "bmr",
            "height",
            "weight",
            "cohabitants",
            "screen_hours",
            "stress_level",
            "defecate_quantity_per_day",
            "general_hunger_level",
            "morning_hunger_level",
            "evening_hunger_level",
            "mid_hunger_level",
        ]

        cols_train = (
            NUTRI_MACRO_VARS
            + NUTRI_MICRO_VARS
            + NUTRI_CFG_VARS
            + NUTRI_FG_VARS
            + NUTRI_DI_VARS
            + AMOUNT_VARS
            + cv_vars
            + PERSONAL_VARS
            + categ_cols_clf
        )

        # Convert categorical columns to numeric
        v = convert_to_numeric(v, categ_cols_clf)

        # Create quartiles and filter for Q1 and Q4
        v[col_target + "_Quartile"] = create_quartiles(v, col_target)
        v = v[v[col_target + "_Quartile"].isin(["Q1", "Q4"])]

        # Select relevant columns
        v = v[cols_train + [col_target + "_Quartile"]]

        print(f"Data shape: {v.shape}")

        # Run classification iterations
        res_clf_auroc = []
        res_clf_auprc = []
        res_clf_featImp = []

        for i in tqdm(range(n_iterations)):
            results = train_and_evaluate_classifier(
                v,
                col_target + "_Quartile",
                test_size=0.2,
                random_state=i,
                n_estimators=1000,
                plot_conf_matrix=False,
                plot_feature_importance=False,
            )
            res_clf_auroc.append(results[0])  # ROC AUC
            res_clf_auprc.append(results[1])  # PR AUC
            res_clf_featImp.append(
                results[2].set_index("Feature")
            )  # Feature importance

        print(f"{col_target} average performance: {round(np.mean(res_clf_auroc), 3)}")
        diversity_clf_res[process_string(col_target)] = res_clf_auroc
        print(f"{col_target} average PR AUC: {round(np.mean(res_clf_auprc), 3)}")
        diversity_clf_auprc[process_string(col_target)] = res_clf_auprc

        # Process feature importance
        avg_featImp = (
            pd.concat(res_clf_featImp)
            .groupby(level=0)
            .mean()
            .sort_values(by="Importance", ascending=False)
        )
        avg_featImp.rename(columns={"Importance": col_target}, inplace=True)
        diversity_clf_featImp[col_target] = avg_featImp

    return diversity_clf_res, diversity_clf_auprc, diversity_clf_featImp


def combine_feature_importance(diversity_clf_featImp, metrics):
    """
    Combine feature importance results for all metrics.

    Parameters:
    - diversity_clf_featImp: dict of feature importance results
    - metrics: list of metrics used

    Returns:
    - Combined DataFrame of feature importance
    """
    result = diversity_clf_featImp[metrics[0]]
    for metric in metrics[1:]:
        result = result.merge(diversity_clf_featImp[metric], on="Feature")

    return result.sort_values(metrics, ascending=False)


def main():
    """Main function to run diversity analysis."""
    # Load data
    meta = pd.read_csv("../../data/fay_meta_diets.csv")

    # Define diversity metrics
    diversity_metrics = [
        "faith_pd",
        "shannon_entropy",
        "observed_features",
        "pielou_evenness",
    ]

    # Run analysis
    diversity_clf_res, diversity_clf_auprc, diversity_clf_featImp = (
        analyze_diversity_metrics(meta, diversity_metrics, n_iterations=50)
    )

    # Combine and sort feature importance results
    diversity_clf_featImp_df = combine_feature_importance(
        diversity_clf_featImp, diversity_metrics
    )

    # Save results
    print("\nSaving results...")
    pd.DataFrame(diversity_clf_res).to_csv(
        "./results/classifier_performance_diversity_auroc.csv"
    )
    pd.DataFrame(diversity_clf_auprc).to_csv(
        "./results/classifier_performance_diversity_auprc.csv"
    )
    diversity_clf_featImp_df.to_csv("./results/clr_featImp_diversity.csv")
    print("Analysis complete!")


if __name__ == "__main__":
    main()
