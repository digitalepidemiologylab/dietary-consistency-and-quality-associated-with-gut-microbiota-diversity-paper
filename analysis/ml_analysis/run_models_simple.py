"""Main script to run the ML analysis."""

import pandas as pd

# from config.variables import (
#     ALL_VARS,
#     get_cv_vars,
# )
from utils.data_processing import combine_feature_importances
from utils.model_utils import (
    model_feature_classifier_performance,
    model_feature_regressor_performance,
)

# import pickle


# Analysis parameters
TOP_N_FEATS = 40
NUM_ITER_CLR = 20  # Modify this to reduce the number of iterations!
NUM_ITER_REG = 20  # Modify this to reduce the number of iterations!


def main():
    """Run the main analysis pipeline."""
    # Load data
    meta = pd.read_csv("../../data/fay_meta_diets.csv")
    counts_data = pd.read_csv("../../data/counts_data_with_taxonomy.csv", index_col=0)

    # Preprocess urbanity
    meta["urbanity"] = meta["urbanity"].map(
        lambda i: "urban" if i == "urban" else "non-urban"
    )

    # Get CV variables
    # cv_vars = get_cv_vars(meta)
    # variables_to_analyze = list(ALL_VARS) + cv_vars

    # Initialize results containers
    performance_reg_all_mb = {}
    performance_auroc_all_mb = {}
    performance_auprc_all_mb = {}
    # performance_precision_all_mb = {}
    # performance_recall_all_mb = {}
    featImp_top_all_mb = pd.DataFrame()

    # Run analysis for each variable
    for col in ["vegetables_fruits", "oils_fats_nuts"]:
        # for col in variables_to_analyze:  # Modify this to run a subset of the variables!
        print(f"\nProcessing variable: {col}")

        # Set up classification parameters
        if col == "age_group_2":
            levels = ["<35", ">50"]
            make_quartiles = False
        elif col == "language":
            levels = ["latin", "german"]
            make_quartiles = False
        elif col == "urbanity":
            levels = ["urban", "non-urban"]
            make_quartiles = False
        elif col == "swiss_citizen":
            levels = ["swiss", "foreign"]
            make_quartiles = False
        elif col == "smoking":
            levels = ["smoker", "non-smoker"]
            make_quartiles = False
        else:
            levels = ["Q1", "Q4"]
            make_quartiles = True

        # Run classifier
        (
            auroc_iters,
            auprc_iters,
            featImp_iters,
            fpr_iters,
            tpr_iters,
            precision_iters,
            recall_iters,
        ) = model_feature_classifier_performance(
            meta,
            counts_data,
            col,
            levels=levels,
            num_iter=NUM_ITER_CLR,
            make_quartiles=make_quartiles,
            plot_conf_matrix=False,
            plot_feature_importance=False,
        )

        # Store classification results
        performance_auroc_all_mb[col] = auroc_iters
        performance_auprc_all_mb[col] = auprc_iters
        # performance_precision_all_mb[col] = precision_iters
        # performance_recall_all_mb[col] = recall_iters

        # Process feature importances
        featImp_iters_combined = combine_feature_importances(featImp_iters).set_index(
            "Feature"
        )
        median_featimps_top_n = featImp_iters_combined.median(axis=1).sort_values(
            ascending=False
        )[:TOP_N_FEATS]
        median_featimps_top_n = median_featimps_top_n[median_featimps_top_n > 0]
        median_featimps_top_n.name = col
        featImp_top_all_mb = pd.concat(
            [featImp_top_all_mb, median_featimps_top_n], axis=1
        )

        # Run regression if applicable
        if col == "age_group_2":
            col = "age"
        elif col not in ["language", "urbanity", "swiss_citizen", "smoking", "income"]:
            print(f"Running regression for {col}")
            spearman_corrs = model_feature_regressor_performance(
                meta,
                counts_data,
                col,
                sample_id_col="sample-id",
                num_iter=NUM_ITER_REG,
                verbose=True,
            )
            performance_reg_all_mb[col] = spearman_corrs


if __name__ == "__main__":
    main()
