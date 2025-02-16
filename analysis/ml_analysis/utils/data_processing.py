import pandas as pd


def create_quartiles(df, column_name, q=4):
    """
    Create quartiles for a numerical column in a pandas DataFrame.

    Parameters:
    - df: pandas.DataFrame containing the data.
    - column_name: String, the name of the column to be binned into quartiles.
    - q: Integer, the number of quantiles. Default is 4 (quartiles).

    Returns:
    - A pandas Series with the quartile assignment for each entry in the column.
    """
    quartiles = pd.qcut(df[column_name], q, labels=[f"Q{i}" for i in range(1, q + 1)])
    return quartiles.astype(str)


def combine_feature_importances(dfs):
    """
    Combine multiple DataFrames containing feature importances.

    Parameters:
    - dfs (list of pd.DataFrame): List of DataFrames to combine.

    Returns:
    - pd.DataFrame: Combined DataFrame with unique 'Feature' column and
                   separate 'importance' columns for each input DataFrame.
    """
    combined_df = None

    for i, df in enumerate(dfs):
        # Rename 'importance' column uniquely
        df_renamed = df.rename(columns={"Importance": f"importance_{i}"})
        df_renamed = df_renamed[:50]

        if combined_df is None:
            combined_df = df_renamed
        else:
            # Merge with the combined DataFrame on 'feature', using outer join
            combined_df = pd.merge(combined_df, df_renamed, on="Feature", how="outer")

    return combined_df.fillna(0)


def process_string(
    s,
    ignore_vars=[
        "PDI_Quintile",
        "hPDI_Quintile",
        "HEI",
        "BMI",
    ],
    newLineSep=3,
):
    if s in ignore_vars:
        return s
    if s == "defecate_quantity_per_day":
        return "Defecation Frequency"
    s = s.replace("_fg", "")
    # Step 1 & 2: Split the string by "_" and replace "_" with a space, then capitalize the first letter
    parts = s.replace("_eaten", "").split("_")
    # capitalized_parts = [part.capitalize() for part in parts]
    capitalized_parts = [part[0].upper() + part[1:] if part else "" for part in parts]

    # Step 3: If there are more than 3 items, insert "\n" in the middle
    if newLineSep and len(capitalized_parts) > newLineSep and "CV" not in s:
        mid_index = len(capitalized_parts) // 2
        processed_string = (
            " ".join(capitalized_parts[:mid_index])
            + "\n"
            + " ".join(capitalized_parts[mid_index:])
        )
    elif "CV" in s:
        processed_string = (
            capitalized_parts[0] + " (" + " ".join(capitalized_parts[1:]) + ")"
        )
    else:
        processed_string = " ".join(capitalized_parts)

    return processed_string
