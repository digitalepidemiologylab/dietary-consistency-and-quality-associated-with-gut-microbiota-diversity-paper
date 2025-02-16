import pandas as pd
from skbio.stats.composition import clr

########################################################
# Loading Prevalence data for the ASV
########################################################
prevalence = pd.read_csv("../../data/prevalence_microbes.csv", index_col=0).squeeze()
dict_ASV_names = dict(
    zip(
        prevalence.sort_values(ascending=False).index,
        ["ASV_" + str(i) for i in range(len(prevalence))],
    )
)

########################################################
# Loading Taxonomy data for the ASV
########################################################
path_asv_taxonomy = "../../qiime/taxonomy_rarefied-table_2024_09/taxonomy.tsv"
# path_asv_taxonomy = "../../qiime/taxonomy_rarefied-table_2022_10/taxonomy.tsv"
otuID_taxonomy = pd.read_csv(path_asv_taxonomy, sep="\t", index_col=0)

########################################################
########################################################


def transform_counts_data(counts_data, method="clr"):
    """
    Transform the counts data using either CLR or Relative Abundance followed by log transformation.

    Parameters:
    counts_data (pd.DataFrame): The input counts data.
    method (str): The transformation method to use. Options are 'clr' for CLR transformation and
                  'relative_abundance' for relative abundance followed by log transformation.

    Returns:
    pd.DataFrame: The transformed counts data.
    """
    if method == "clr":
        # Perform CLR transformation
        df_mb = pd.DataFrame(clr(counts_data.replace(0, 1)))
        df_mb.index = counts_data.index
        df_mb.columns = counts_data.columns
    elif method == "relative_abundance":
        # Perform relative abundance transformation followed by log transformation
        df_mb = counts_data.div(counts_data.sum(axis=1), axis=0)  # Relative abundance
        # df_mb = np.log10(df_mb + 1e-6)  # Log transformation
    else:
        raise ValueError("Invalid method. Choose either 'clr' or 'relative_abundance'.")

    return df_mb


def filter_microbes_by_prevalence(df, count_threshold=0, prevalence_threshold=0.5):
    """
    Filters out microbes based on prevalence across samples.

    Parameters:
    - df (pd.DataFrame): DataFrame with samples on rows, microbes on columns, and read counts as values.
    - count_threshold (int): The minimum read count for a microbe to be considered present in a sample.
    - prevalence_threshold (float): The minimum prevalence (proportion of samples where a microbe is present)
      for a microbe to be retained.

    Returns:
    - pd.DataFrame: A filtered DataFrame with low-prevalence microbes removed.
    """
    # Calculate prevalence for each microbe
    prevalence = (df > count_threshold).sum() / df.shape[0]

    # Filter microbes based on prevalence threshold
    microbes_to_keep = prevalence[prevalence >= prevalence_threshold].index

    filtered_df = df[microbes_to_keep]

    return filtered_df, prevalence


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


def shorten_taxa_name(taxa_name):
    """
    Shorten the name of a taxa to the genus or species level if possible.
    """
    if taxa_name.startswith("species__"):
        return taxa_name.split("__")[1]
    elif taxa_name.startswith("genus__"):
        return taxa_name.split("__")[1]
    elif taxa_name.startswith("family__"):
        return taxa_name.split("__")[1]
    else:
        return taxa_name


def redefined_taxa_short_name(taxa_name, level="species"):
    """
    Shorten the name of a taxa to the genus or species level if possible.
    """

    regular = shorten_taxa_name(extract_taxa_name(taxa_name, level))

    if (
        regular.startswith("g__COE1")
        or regular.startswith("s__UBA")
        or regular.startswith("g__G11")
        or regular.startswith("g__C-53")
    ):
        return shorten_taxa_name(extract_taxa_name(taxa_name, "family")) + ";" + regular
    elif (
        regular.startswith("s__CAG")
        or regular.startswith("s__PeH")
        or regular.startswith("g__SFM")
        or regular.startswith("s__QALR01")
    ):
        return shorten_taxa_name(extract_taxa_name(taxa_name, "order")) + ";" + regular

    return regular


def extract_taxa_name(taxonomy_string, level="species"):
    """
    Extracts the name at a specified taxa level from a taxonomy string.
    If the name at that level is absent, it searches higher levels until a name is found.
    """
    # Define the order of levels to facilitate searching upwards
    levels_order = ["domain", "phylum", "class", "order", "family", "genus", "species"]
    levels_abbr = {
        "domain": "d",
        "phylum": "p",
        "class": "c",
        "order": "o",
        "family": "f",
        "genus": "g",
        "species": "s",
    }

    # Split the taxonomy string into components
    taxa_parts = taxonomy_string.split(";")

    # Dictionary to hold each part of the taxonomy with its level as key
    taxa_dict = {}
    for part in taxa_parts:
        taxa_level, _, taxa_name = part.partition("__")
        if taxa_level:  # Check that taxa_level is not empty
            taxa_dict[taxa_level[0]] = taxa_name

    # Search for the desired level and upwards if necessary
    # level_abbr = levels_abbr.get(level, "")
    for i in range(levels_order.index(level), -1, -1):
        current_level = levels_order[i]
        if (
            levels_abbr[current_level] in taxa_dict
            and taxa_dict[levels_abbr[current_level]]
        ):
            return (
                f"{levels_abbr[current_level]}__{taxa_dict[levels_abbr[current_level]]}"
            )

    return "Name not found"


def extract_taxonomy_level(taxonomy_str, level):
    """
    Extracts the taxonomy information at a specified level from a given taxonomy string.

    Parameters:
    - taxonomy_str (str): The taxonomy string to be searched.
    - level (str): The taxonomy level to extract (e.g., 'd', 'p', 'c', 'o', 'f', 'g', 's').

    Returns:
    - str: The name of the taxonomy at the specified level, or an empty string if not found.
    """
    # Split the taxonomy string into parts
    parts = taxonomy_str.split(";")

    # Search for the desired level
    for part in parts:
        if part.startswith(level + "__"):
            # Extract and return the taxonomy name without the level prefix
            return part.split("__")[1]
    # Return an empty string if the level is not found
    return ""


def summarize_microbe_foodvar_relationship(mb_data, meta, variables, bac_name):
    """
    Summarize the relationship between microbial abundance and dietary variables.

    Parameters:
    - mb_data: DataFrame with counts data, columns are samples.
    - meta: DataFrame with metadata, indexed by "sample-id".
    - variables: List of dietary variables to analyze.
    - bac_name: Name of the bacterium to analyze.

    Returns:
    - A DataFrame summarizing the median values for the top and bottom quartiles and Spearman correlation.
    """
    # Extract the bacterium data
    bac = [i for i in mb_data.columns if bac_name in i][0]
    print(bac)
    bac_meta = meta.merge(mb_data[[bac]], left_on="sample-id", right_index=True)

    summary_all = {"foodvar": [], "Q4_median": [], "Q1_median": [], "corr": []}

    for c in variables:
        newcol = f"{c}_Quartile"
        bac_meta[newcol] = create_quartiles(bac_meta, c)

        q4_median = bac_meta[bac_meta[newcol] == "Q4"][bac].median()
        q1_median = bac_meta[bac_meta[newcol] == "Q1"][bac].median()

        summary_all["foodvar"].append(process_string(c))
        summary_all["Q4_median"].append(q4_median)
        summary_all["Q1_median"].append(q1_median)
        summary_all["corr"].append(
            bac_meta[[c, bac]].corr(method="spearman").iloc[0, 1]
        )  # Spearman correlation
        summary_all["bac_fullname"] = bac
        summary_all["bac"] = bac_name

    return pd.DataFrame(summary_all)
