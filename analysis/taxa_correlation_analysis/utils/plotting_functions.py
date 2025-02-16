import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from textwrap import wrap
from statsmodels.stats.multitest import multipletests
from collections import Counter
import pingouin as pg
from tqdm import tqdm

from .data_processing import (
    shorten_taxa_name,
    extract_taxa_name,
    otuID_taxonomy,
    dict_ASV_names,
)


def taxonID_shortName(featureID, level="genus"):
    """
    Shorten the name of a taxa to the genus or species level if possible.
    """

    taxa_name = otuID_taxonomy.loc[featureID].values[0].replace("; ", ";")
    asv_id = dict_ASV_names[featureID]

    regular = shorten_taxa_name(extract_taxa_name(taxa_name, level))
    # regular = regular + " (" + asv_id + ")"
    regular = asv_id + " (" + regular + ")"

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


def create_polar_plot(
    summary_df,
    ax,
    prevalence,
    cmap=plt.cm.RdYlGn,
    show_medians_text=True,
    q1_dotsize=50,
    paneltext=None,
    paneltext_pos=(-0.05, 1.1),
    taxon_type="regular",
):

    ANGLES = np.linspace(0.05, 2 * np.pi - 0.05, len(summary_df), endpoint=False)
    LENGTHS = summary_df["Q4_median"].values
    Q1_MEDIAN = summary_df["Q1_median"].values
    FOODVAR = summary_df["foodvar"].values
    CORR_SP = summary_df["corr"].values

    norm = mpl.colors.Normalize(vmin=CORR_SP.min(), vmax=CORR_SP.max())
    COLORS = cmap(norm(CORR_SP))

    # Set background color
    # fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Set the limits
    upperlim = np.ceil(
        max(summary_df["Q4_median"].max(), summary_df["Q1_median"].max())
    )
    lowerlim = np.floor(
        min(summary_df["Q4_median"].min(), summary_df["Q1_median"].min())
    )

    # Radial axis configuration
    if lowerlim < 0:
        y_ticks_list = list(range(-1, int(upperlim + 1)))
        ylimlower = np.floor(lowerlim) - 1
    else:
        y_ticks_list = list(range(1, int(upperlim + 1)))  # np.linspace(0, upperlim, 4)
        ylimlower = -1
    # Configure the polar plot
    ax.set_theta_offset(1.2 * np.pi / 2)
    ax.set_ylim(ylimlower, upperlim + 0.08 * upperlim)

    vline_color = "#303030"
    q1_dot_color = "#303030"
    # Add geometries to the plot
    ax.bar(ANGLES, LENGTHS, color=COLORS, alpha=0.9, width=0.52, zorder=10)
    ax.vlines(
        ANGLES,
        ylimlower + 1,
        upperlim,
        color=vline_color,
        ls=(0, (4, 4)),
        zorder=11,
        linewidth=0.5,
    )
    ax.scatter(ANGLES, Q1_MEDIAN, s=q1_dotsize, color=q1_dot_color, zorder=11)

    # Add labels for the FOODVAR
    FOODVAR = ["\n".join(wrap(r, 5, break_long_words=False)) for r in FOODVAR]
    ax.set_xticks(ANGLES)
    ax.set_xticklabels(FOODVAR, size=11)
    ax.xaxis.grid(False)

    ax.yaxis.grid(True, linestyle="-", color="black", linewidth=0.5, alpha=0.5)

    ax.set_yticklabels([])
    ax.set_yticks([0] + y_ticks_list)

    # Remove spines
    ax.spines["start"].set_color("none")
    ax.spines["polar"].set_color("none")

    # Y-axis labels
    PAD = 0
    for yt in y_ticks_list:
        ax.text(-0.2 * np.pi / 2, yt + PAD, f"{yt}", ha="center", size=10)

    # Add text to explain the meaning of the height of the bar and the height of the dot
    if show_medians_text:
        max_length = summary_df["Q4_median"].max()
        middle_length = max_length / 2
        ax.text(
            ANGLES[0],
            max_length + 0.04 * max_length,
            "Q4 Median",
            rotation=21,
            ha="center",
            va="center",
            size=8.8,
            zorder=12,
        )
        ax.text(
            ANGLES[0] + 0.112,
            middle_length,
            "Q1 Median",
            rotation=-69,
            ha="center",
            va="center",
            size=8.8,
            zorder=12,
        )

    # Subplot title
    bac_name_string = summary_df["bac"].values[0]
    if taxon_type == "ASV":
        ax.set_title(
            taxonID_shortName(bac_name_string, level="genus"),
            size=12,
            fontweight="bold",
            pad=30,
            fontstyle="italic",
        )
    else:
        ax.set_title(
            bac_name_string, size=12, fontweight="bold", pad=30, fontstyle="italic"
        )

    # Centre text
    bac_fullname = summary_df["bac_fullname"].values[0]
    center_text = str(int(100 * prevalence[bac_fullname])) + "%"
    ax.text(
        0,
        ylimlower,
        center_text,
        ha="center",
        va="center",
        size=11,
        color="black",
        zorder=11,
        transform=ax.transData,
    )

    if paneltext:
        ax.text(
            paneltext_pos[0],
            paneltext_pos[1],
            paneltext,
            fontsize=16,
            fontweight="bold",
            transform=ax.transAxes,
        )


########################################################################################
# Ancestry color mapping
########################################################################################


def filter_correlations(mb_data, meta, var, threshold=0.1):
    """
    Merges two dataframes, calculates Spearman correlations for a specified variable,
    sorts the correlations, removes NaN values, and filters out correlations below
    a specified threshold.

    Parameters:
    - mb_data: pandas DataFrame, the primary data with multiple columns for correlation.
    - meta: pandas DataFrame, contains metadata including the 'sample-id' and the variable of interest.
    - var: string, the column name in meta DataFrame to correlate against.
    - threshold: float, the minimum absolute value of correlation to include in the result.

    Returns:
    - A pandas Series with variables sorted by their correlation to the specified variable,
      excluding any with absolute correlation values less than the threshold.
    """
    merged_data = mb_data.merge(meta[[var]], left_index=True, right_index=True)

    # # Calculate Spearman correlations with the specified variable
    correlations = merged_data.corr(method="spearman")[var].sort_values()

    # Remove NaN values
    correlations = correlations.dropna()

    # Filter out correlations below the threshold
    filtered_correlations = correlations[correlations.abs() >= threshold]

    return filtered_correlations.drop(var)


def do_partial_correlations(
    mb_data, meta, var, covariates=["age", "bmi"], corr_threshold=0.1, method="spearman"
):
    """
    Merges two dataframes, calculates Spearman correlations for a specified variable,
    applies FDR correction, sorts the correlations, removes NaN values, and filters
    out correlations below a specified threshold.

    Parameters:
    - mb_data: pandas DataFrame, the primary data with multiple columns for correlation.
    - meta: pandas DataFrame, contains metadata including the variable of interest.
    - var: string, the column name in meta DataFrame to correlate against.
    - covariates: list of strings, the names of columns to adjust for in the partial correlation.
    - corr_threshold: float, the minimum absolute value of correlation to include in the result.

    Returns:
    - A pandas DataFrame with microbes sorted by their correlation to the specified variable,
      excluding any with absolute correlation values less than the threshold, including FDR-adjusted p-values.
    """
    merged_data = mb_data.merge(
        meta[[var] + covariates], left_index=True, right_index=True
    )

    all_res = pd.DataFrame()
    for microbe in mb_data.columns:
        if np.isclose(merged_data[microbe].var(), 0):
            continue
        microbe_res = pg.partial_corr(
            data=merged_data, x=microbe, y=var, covar=covariates, method=method
        )
        microbe_res["microbe"] = microbe
        microbe_res["feature"] = var
        all_res = pd.concat([all_res, microbe_res])

    # Apply FDR correction
    _, corrected_pvals, _, _ = multipletests(all_res["p-val"], method="fdr_bh")
    all_res["corrected_pval"] = corrected_pvals

    # Filter based on threshold and corrected p-values
    significant_results = all_res.loc[(abs(all_res["r"]) > corr_threshold)]

    # Sort by correlation magnitude (absolute value)
    significant_results = significant_results.sort_values(
        by="r", key=abs, ascending=False
    )

    return significant_results


def perform_partial_correlations(
    counts_data,
    metadata,
    variables,
    covariates=["age", "bmi"],
    corr_threshold=0.1,
    top_n_common=50,
    method="spearman",
):
    partialcorr_df = pd.DataFrame()
    for var in tqdm(variables):
        filtered_corr = do_partial_correlations(
            counts_data,
            metadata.set_index("sample-id"),
            var,
            covariates=covariates,
            corr_threshold=corr_threshold,
            method=method,
        )
        partialcorr_df = pd.concat([partialcorr_df, filtered_corr])

    corr_pivot = partialcorr_df.pivot_table(
        index="microbe", columns="feature", values="r"
    )
    # corr_pivot.columns = [i.replace("_eaten", "") for i in corr_pivot.columns]

    # Select top n rows (microbes) with most non-null values
    if top_n_common > 0:
        most_common_rows = (
            corr_pivot.notnull()
            .sum(axis=1)
            .sort_values(ascending=False)
            .head(top_n_common)
            .index
        )
        corr_pivot = corr_pivot.loc[most_common_rows].fillna(0)

    return partialcorr_df, corr_pivot


def extract_taxonomy_mapping(dataframe, taxonomy_level, taxon_type="regular"):
    """
    Extracts taxonomy mapping from index strings to a specified taxonomy level.

    Parameters:
    - dataframe: pandas DataFrame with index containing taxonomy strings.
    - taxonomy_level: string, one of 'family', 'class', 'order' indicating the desired taxonomy level.

    Returns:
    - A dictionary mapping full taxonomy strings to their specified taxonomy level.
    """
    taxonomy_level_prefix = {
        "family": "f__",
        "class": "c__",
        "order": "o__",
    }

    # Check if the requested taxonomy level is valid
    if taxonomy_level not in taxonomy_level_prefix:
        raise ValueError(
            f"Invalid taxonomy level: {taxonomy_level}. Choose from 'family', 'class', 'order'."
        )

    prefix = taxonomy_level_prefix[taxonomy_level]
    taxonomy_mapping = {}

    for index_string in dataframe.index:

        if taxon_type == "ASV":
            featureID = index_string
            index_string = otuID_taxonomy.loc[index_string].values[0].replace("; ", ";")

        # Split the string into components based on semicolons
        components = index_string.split(";")

        # Extract the component that starts with the prefix corresponding to the desired taxonomy level
        taxonomy_component = next(
            (component for component in components if component.startswith(prefix)),
            None,
        )

        # Map the full string to the extracted taxonomy component
        # If the component is not found, you can choose to handle it as you see fit (e.g., map to 'Unknown')
        if taxon_type == "ASV":
            taxonomy_mapping[featureID] = (
                taxonomy_component if taxonomy_component else "Unknown"
            )
        else:
            taxonomy_mapping[index_string] = (
                taxonomy_component if taxonomy_component else "Unknown"
            )

    print(len(taxonomy_mapping), len(dataframe))

    return taxonomy_mapping


def dot_size(p_val):
    if p_val < 0.001:
        return "***"  # Large dot
    elif p_val < 0.01:
        return "**"  # Medium dot
    elif p_val < 0.05:
        return "*"  # Small dot
    else:
        return ""  # No dot


def create_annot_matrix(
    corr_across_feats_df, partialcorr_across_feats_df, species_level="species"
):
    """
    Creates an annotation matrix for a heatmap from partial correlation data.

    Parameters:
    - corr_across_feats_df: DataFrame containing Spearman correlation coefficients.
    - partialcorr_across_feats_df: DataFrame containing partial correlations and features.
    - species_level: The taxonomic level used for species identification.

    Returns:
    - annot_matrix: A DataFrame with the same indices and columns as corr_across_feats_df
                    containing strings for annotations.
    """
    # Initialize an empty DataFrame with the same structure as corr_across_feats_df
    annot_matrix = pd.DataFrame(
        "", index=corr_across_feats_df.index, columns=corr_across_feats_df.columns
    )

    # Populate the annotation matrix with data from partial correlations
    for _, row in partialcorr_across_feats_df.iterrows():
        # microbe_short = redefined_taxa_short_name(row['microbe'])
        microbe_short = taxonID_shortName(row["taxonID"])
        # microbe_short = shorten_taxa_name(extract_taxa_name(row['microbe'], species_level))
        feature_short = row["feature"]  # .replace("_eaten", "")
        # Check if the current microbe and feature exist in the correlation matrix's index and columns
        if (
            microbe_short in annot_matrix.index
            and feature_short in annot_matrix.columns
        ):
            # Update the corresponding cell in the annotation matrix
            annot_value = dot_size(
                row["corrected_pval"]
            )  # Define or adjust `dot_size` as needed
            annot_matrix.at[microbe_short, feature_short] = annot_value

    return annot_matrix


def generate_ancestry_color_mapping(
    corr_df,
    taxonomy_level="family",
    top_taxonomy_legend_colours=8,
    species_level="species",
    taxa_palette="Dark2",
):
    """
    Generates a mapping of taxonomy to colors for plotting and updates correlation dataframe indices.

    Parameters:
    - corr_df: DataFrame containing correlation data with taxa names as indices.
    - taxonomy_level: The taxonomy level used for mapping (e.g., 'family').
    - top_taxonomy_legend_colours: Number of unique taxonomy colors to show in the legend.
    - species_level: The species level used for mapping and index shortening.

    Returns:
    - ancestry_colour_mapping: A dictionary mapping taxonomy to colors.
    - updated_corr_df: Updated correlation DataFrame with shortened taxa names as indices.
    - ancestor_mapping: A dictionary mapping shortened taxa names to their ancestors.
    """
    # Extract taxonomy mapping and update indices
    ancestor_mapping = extract_taxonomy_mapping(
        corr_df, taxonomy_level, taxon_type="ASV"
    )

    updated_corr_df = corr_df.copy()
    # updated_corr_df.index = updated_corr_df.index.map(lambda i: shorten_taxa_name(extract_taxa_name(i, species_level)))
    # updated_corr_df.index = updated_corr_df.index.map(redefined_taxa_short_name)
    updated_corr_df.index = updated_corr_df.index.map(taxonID_shortName)

    # Update the ancestor mapping with shortened names
    # ancestor_mapping = {redefined_taxa_short_name(k): v for k, v in ancestor_mapping.items()}
    ancestor_mapping = {taxonID_shortName(k): v for k, v in ancestor_mapping.items()}

    # Determine top taxonomy for legend
    top_taxonomy_legend_names_to_show = []
    top_taxonomy_legend_names_to_hide = []
    for e, v in enumerate(
        sorted(
            Counter(ancestor_mapping.values()).items(),
            key=lambda item: item[1],
            reverse=True,
        )
    ):
        if v[1] == 1:
            top_taxonomy_legend_names_to_hide.append(v[0])
        if e < top_taxonomy_legend_colours:
            top_taxonomy_legend_names_to_show.append(v[0])
        else:
            top_taxonomy_legend_names_to_hide.append(v[0])

    # Generate color mapping
    ancestry_colour_mapping = dict(
        zip(
            top_taxonomy_legend_names_to_show,
            sns.color_palette(taxa_palette, len(top_taxonomy_legend_names_to_show)),
        )
    )
    for k in top_taxonomy_legend_names_to_hide:
        ancestry_colour_mapping[k] = "grey"

    return ancestry_colour_mapping, updated_corr_df, ancestor_mapping


def extract_clustermap_heatmap_data(
    corr_across_feats_df, annot_matrix, figsize=(10, 14)
):
    # Perform clustering and get the ordered rows and columns
    clustergrid = sns.clustermap(
        corr_across_feats_df,
        cmap="PiYG",
        center=0,
        figsize=figsize,
        annot=False,  # We'll add annotations manually later
        cbar_kws={"label": "Spearman Correlation", "shrink": 0.5},
        linewidths=0.05,
        linecolor="gray",
        row_cluster=True,
        col_cluster=True,
        dendrogram_ratio=(0.1, 0.1),
    )

    # Get the order of rows and columns from the clustering
    row_order = clustergrid.dendrogram_row.reordered_ind
    col_order = clustergrid.dendrogram_col.reordered_ind

    # Create new DataFrame with ordered data for heatmap
    ordered_corr_df = corr_across_feats_df.iloc[row_order, col_order]
    ordered_annot_matrix = annot_matrix.iloc[row_order, col_order]

    # Close the clustermap figure to avoid showing it
    plt.close(clustergrid.fig)

    return ordered_corr_df, ordered_annot_matrix, row_order, col_order


def draw_heatmap_from_clustermap_data(
    ax,
    ordered_corr_df,
    ordered_annot_matrix,
    ancestry_colour_mapping,
    ancestor_mapping,
    legend_patches,
    cmap="PiYG",
    paneltext=None,
    paneltext_pos=(-0.05, 1.15),
):
    """
    Draws heatmap derived from clustermap data on a given Axes object,
    including legends and adjusted colorbar.

    Parameters:
    - ax: matplotlib Axes object where the heatmap will be drawn.
    - ordered_corr_df: DataFrame of ordered correlation data for heatmap.
    - ordered_annot_matrix: DataFrame of annotations corresponding to ordered_corr_df.
    - ancestry_colour_mapping: Dict mapping taxa groups to colors for legend.
    - ancestor_mapping: Dict mapping individual taxa to their group.
    - legend_patches: List of matplotlib.patches.Patch objects for the significance levels legend.
    """

    sns.heatmap(
        ordered_corr_df,
        cmap=cmap,
        center=0,
        ax=ax,
        annot=ordered_annot_matrix,
        fmt="",
        annot_kws={"weight": "bold", "fontsize": 12},
        # vmin=-0.25, vmax=0.3,  # Set the color scale limits
        cbar=False,  # Disable the automatic colorbar
        linewidths=0.05,
        linecolor="gray",
    )

    # Remove the default y-axis label
    ax.set_ylabel("")

    # Create a new colorbar with the heatmap's colormap
    norm = plt.Normalize(
        vmin=ordered_corr_df.min().min(), vmax=ordered_corr_df.max().max()
    )
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    # Create the colorbar at the top of the heatmap
    colorbar_position_y = ax.get_position().y1 + 0.015
    colorbar_position_x = ax.get_position().x0
    cbar_ax = ax.figure.add_axes(
        [colorbar_position_x, colorbar_position_y, ax.get_position().width - 0.3, 0.01]
    )  # x, y, width, height
    cbar = ax.figure.colorbar(
        sm, cax=cbar_ax, orientation="horizontal", label="Spearman Correlation"
    )

    # Customize the colorbar
    cbar.outline.set_visible(False)  # Remove the colorbar border
    cbar.ax.xaxis.set_ticks_position("top")
    cbar.ax.xaxis.set_label_position("top")
    cbar.ax.tick_params(width=0.50)  # Remove the ticks of the colorbar if needed

    for label in ax.get_xticklabels():
        label.set_fontsize(11)

    # Adjust annotations based on ancestor mapping
    for label in ax.get_yticklabels():
        label_text = label.get_text()
        if label_text in ancestor_mapping:
            label.set_color(ancestry_colour_mapping[ancestor_mapping[label_text]])
            label.set_fontstyle("italic")
    plt.setp(ax.get_yticklabels(), fontsize=9)

    # Add taxonomy legend
    reduced_ancestry_colour_mapping = {
        k: v for k, v in ancestry_colour_mapping.items() if v != "grey"
    }
    reduced_ancestry_colour_mapping["Others"] = "grey"

    legend_handles = [
        mpatches.Patch(color=color, label=label)
        for label, color in reduced_ancestry_colour_mapping.items()
    ]
    leg1 = ax.legend(
        handles=legend_handles,
        title="Taxonomy",
        fontsize=9,
        bbox_to_anchor=(-0.38, -0.01),
        loc="upper left",
        frameon=True,
    )
    ax.add_artist(leg1)  # Add the first legend manually

    # Add significance levels legend
    if legend_patches:
        leg2 = ax.legend(
            handles=legend_patches,
            title="Significance",
            fontsize=9,
            ncol=len(legend_patches),
            bbox_to_anchor=(0.7, 1.04),
            loc="center",
            frameon=False,
            columnspacing=0.1,
        )
        ax.add_artist(leg2)
    # plt.tight_layout()

    if paneltext:
        # Adjust these parameters to move your panel letter as needed
        ax.text(
            paneltext_pos[0],
            paneltext_pos[1],
            paneltext,
            fontsize=16,
            fontweight="bold",
            transform=ax.transAxes,
        )

    return ax
