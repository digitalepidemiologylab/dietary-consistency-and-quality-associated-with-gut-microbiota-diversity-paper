import pandas as pd


def read_fasta_to_dataframe(fasta_file):
    """
    Reads a FASTA file and returns a DataFrame with hashes (sequence IDs) and sequences.

    Parameters:
    fasta_file (str): Path to the FASTA file.

    Returns:
    pd.DataFrame: DataFrame with 'Hash' and 'Sequence' columns.
    """
    # Initialize lists to store the hashes and sequences
    hashes = []
    sequences = []

    # Read the FASTA file manually
    with open(fasta_file, "r") as file:
        sequence = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if sequence:
                    sequences.append(sequence)
                    sequence = ""
                hashes.append(line[1:])  # Remove '>' and store the hash
            else:
                sequence += line
        sequences.append(sequence)  # Add the last sequence

    # Create and return a DataFrame
    return pd.DataFrame({"Hash": hashes, "Sequence": sequences})


fasta_file_path = "../../qiime/exported_rep_seqs/dna-sequences.fasta"
rdf = read_fasta_to_dataframe(fasta_file_path)
rdict = rdf.set_index("Hash")["Sequence"].to_dict()
del rdf

########################################################
# Differential Abundance Taxa Combining
########################################################
vars_for_cohort_comparison = [
    "energy_kcal_eaten",
    "carb_eaten",
    "fat_eaten",
    "protein_eaten",
    "fiber_eaten",
    "alcohol_eaten",
    "folate_eaten",
    "iron_eaten",
    "phosphorus_eaten",
    "potassium_eaten",
    "HEI",
    "meat_fg_eaten",
    "fruits_fg_eaten",
    "vegetables_fg_eaten",
    "oils_nuts_fg_eaten",
    "coffee_fg_eaten",
    "grains_cereals_fg_eaten",
    "fast_food_fg_eaten",
]

for e, var in enumerate(vars_for_cohort_comparison[:]):
    diff_abun_df = pd.read_csv(
        f"outputs/{var}/results/differential_taxa.tsv", sep="\t", index_col=0
    )
    diff_abun_df.rename(
        columns={
            f"{var}_mean": "Variable_mean",
            f"{var}_std": "Variable_std",
            f"{var}_hdi": "Variable_hdi",
        },
        inplace=True,
    )
    diff_abun_df["type"] = diff_abun_df["Variable_mean"].map(
        lambda i: "numerator" if i > 0 else "denominator"
    )
    diff_abun_df["Variable_name"] = var
    diff_abun_df["Sequence"] = diff_abun_df["Feature"].map(rdict)

    if len(diff_abun_df) < 30:
        print(var, "has fewer ASV")
        continue

    if e == 0:
        diff_abun_df_for_comparison = diff_abun_df
    else:
        diff_abun_df_for_comparison = pd.concat(
            [diff_abun_df_for_comparison, diff_abun_df]
        )

    print(var, "done")


diff_abun_df_for_comparison["Variable_name"] = diff_abun_df_for_comparison[
    "Variable_name"
].map(lambda i: i.replace("fg_eaten", "eaten"))
diff_abun_df_for_comparison.to_csv("Supplementary_File_1.tsv", sep="\t", index=False)
