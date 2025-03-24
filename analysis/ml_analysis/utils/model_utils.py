"""Core modeling functions for classification and regression."""

import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, auc
from sklearn.model_selection import train_test_split

# from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr, spearmanr
import xgboost as xgb

from .data_processing import create_quartiles


def train_and_evaluate_classifier(
    data,
    target_col,
    test_size=0.2,
    random_state=42,
    n_estimators=1000,
    max_depth=6,
    eta=0.005,
    subsample=0.4,
    colsample_bytree=0.8,
    plot_conf_matrix=True,
    plot_feature_importance=True,
):
    """
    Train a classifier and evaluate its performance.

    Parameters:
    - data: DataFrame containing the dataset
    - target_col: String, name of the target column
    - test_size: Float, proportion of dataset for test split
    - random_state: Integer, random seed
    - n_estimators: Integer, number of boosting rounds
    - max_depth: Integer, maximum tree depth
    - eta: Float, learning rate
    - subsample: Float, subsample ratio of training instances
    - colsample_bytree: Float, subsample ratio of columns for each tree
    - plot_conf_matrix: Boolean, whether to plot confusion matrix
    - plot_feature_importance: Boolean, whether to plot feature importance

    Returns:
    - Tuple containing (roc_auc, pr_auc, feature_importances, (fpr, tpr))
    """
    X = data.drop(columns=[target_col])
    y = data[target_col].apply(lambda x: 1 if x == data[target_col].unique()[0] else 0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    classifier = xgb.XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        eta=eta,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        random_state=random_state,
        alpha=0.1,
        n_jobs=-1,
        eval_metric="logloss",
    )

    classifier.fit(X_train, y_train)
    # y_pred = classifier.predict(X_test)
    y_proba = classifier.predict_proba(X_test)[:, 1]

    roc_auc = roc_auc_score(y_test, y_proba, average="weighted")
    fpr, tpr, thresholds = roc_curve(y_test, y_proba)

    precision, recall, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = auc(recall, precision)

    feature_importances = pd.DataFrame(
        {"Feature": X.columns, "Importance": classifier.feature_importances_}
    )
    feature_importances = feature_importances.sort_values(
        by="Importance", ascending=False
    ).reset_index(drop=True)

    return roc_auc, pr_auc, feature_importances, (fpr, tpr), (precision, recall)


def model_feature_classifier_performance(
    meta,
    mb_data,
    target_col,
    levels=None,
    make_quartiles=False,
    num_iter=3,
    plot_conf_matrix=True,
    plot_feature_importance=True,
    verbose=True,
    sample_id_col="sample-id",
    n_estimators=1000,
    max_depth=6,
    eta=0.005,
    subsample=0.4,
    colsample_bytree=0.8,
):
    """
    Model feature classifier performance across multiple iterations.

    Parameters:
    - meta: DataFrame containing metadata
    - mb_data: DataFrame containing features
    - target_col: String, target column name
    - levels: List, specific levels to include
    - make_quartiles: Boolean, whether to create quartiles
    - num_iter: Integer, number of iterations
    - verbose: Boolean, whether to print progress
    - Other parameters same as train_and_evaluate_classifier

    Returns:
    - Tuple containing iterations of (auroc, auprc, feature_importance, curve_data)
    """
    meta_data = meta.copy()
    meta_data.set_index(sample_id_col, inplace=True)
    meta_data = meta_data[meta_data[target_col].notna()]

    data = mb_data.copy()

    if make_quartiles:
        meta_data[target_col + "_Quartile"] = create_quartiles(meta_data, target_col)
        target_col = target_col + "_Quartile"
    if levels:
        meta_data = meta_data[meta_data[target_col].isin(levels)]

    data = meta_data[[target_col]].merge(data, left_index=True, right_index=True)

    if verbose:
        print(target_col, meta_data[target_col].value_counts().to_dict())

    roc_auc_iters = []
    pr_auc_iters = []
    feat_imp_iters = []
    fpr_iters = []
    tpr_iters = []
    precision_iters = {}
    recall_iters = {}

    for i in range(num_iter):
        roc_auc_res, pr_auc_res, feat_imp, (fpr, tpr), (precision, recall) = (
            train_and_evaluate_classifier(
                data,
                target_col,
                test_size=0.2,
                random_state=i,
                n_estimators=n_estimators,
                max_depth=max_depth,
                eta=eta,
                subsample=subsample,
                colsample_bytree=colsample_bytree,
                plot_conf_matrix=plot_conf_matrix,
                plot_feature_importance=plot_feature_importance,
            )
        )
        roc_auc_iters.append(roc_auc_res)
        pr_auc_iters.append(pr_auc_res)
        feat_imp_iters.append(feat_imp)
        fpr_iters.append(fpr)
        tpr_iters.append(tpr)
        precision_iters[i] = precision
        recall_iters[i] = recall

    if verbose:
        print(
            f"Mean ROC AUC: {np.mean(roc_auc_iters):.3f}, "
            f"Stdev: {np.std(roc_auc_iters):.3f}"
        )
        print(
            f"Mean AUPRC: {np.mean(pr_auc_iters):.3f}, "
            f"Stdev: {np.std(pr_auc_iters):.3f}\n"
        )

    return (
        roc_auc_iters,
        pr_auc_iters,
        feat_imp_iters,
        fpr_iters,
        tpr_iters,
        precision_iters,
        recall_iters,
    )


def model_feature_regressor_performance(
    meta,
    mb_data,
    target_col,
    sample_id_col="sample-id",
    objective="reg:squarederror",
    num_iter=3,
    verbose=False,
):
    """
    Model feature regressor performance across multiple iterations.

    Parameters:
    - meta: DataFrame containing metadata
    - mb_data: DataFrame containing features
    - target_col: String, target column name
    - sample_id_col: String, sample ID column name
    - objective: String, XGBoost objective function
    - num_iter: Integer, number of iterations
    - verbose: Boolean, whether to print progress

    Returns:
    - List of Spearman correlations for each iteration
    """
    meta_data = meta.copy()
    meta_data.set_index(sample_id_col, inplace=True)
    meta_data = meta_data[meta_data[target_col].notna()]

    data = mb_data.join(meta_data[[target_col]], how="inner")
    spearman_corrs = []
    pearson_corrs = []

    if data[target_col].mean() < 0.001:
        print("**** Log transforming the target variable:", target_col, "****")
        data[target_col] = np.log10(data[target_col] + 1e-6)

    for seed in range(num_iter):
        X_train, X_test, y_train, y_test = train_test_split(
            data.drop(columns=[target_col]),
            data[target_col],
            test_size=0.2,
            random_state=seed,
        )

        model = xgb.XGBRegressor(
            objective=objective,
            n_estimators=1000,
            learning_rate=0.05,
            random_state=seed,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        pearson_corr, _ = pearsonr(y_test, y_pred)
        spearman_corr, _ = spearmanr(y_test, y_pred)
        spearman_corrs.append(spearman_corr)
        pearson_corrs.append(pearson_corr)

    if verbose:
        print("Data shape:", data.shape)
        print(f"Average Pearson correlation: {np.mean(pearson_corrs):.4f}")
        print(f"Average Spearman correlation: {np.mean(spearman_corrs):.4f}")
        print(f"Std dev Spearman correlation: {np.std(spearman_corrs):.4f}")

    return spearman_corrs
