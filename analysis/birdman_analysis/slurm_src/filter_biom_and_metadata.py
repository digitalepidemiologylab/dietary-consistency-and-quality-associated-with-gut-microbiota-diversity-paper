import biom
import pandas as pd

# Load the BIOM table
biom_path = "data/feature-table.biom"
table = biom.load_table(biom_path)

# Load and preprocess metadata
metadata = pd.read_csv("data/fay_meta_diets.csv")
metadata.rename(columns={"id": "host_subject_id"}, inplace=True)
metadata["host_subject_id"] = "S" + metadata["host_subject_id"].astype(str)
metadata = metadata.set_index("sample-id")

# Find common samples between metadata and biom table
common_samples = set(metadata.index).intersection(table.ids())

print("metadata shape:", metadata.shape)
print("table shape:", table.shape)

# Filter features and samples based on prevalence and common samples
prevalence = table.to_dataframe().clip(upper=1).sum(axis=1)
features_to_keep = prevalence[
    prevalence >= 250
].index.tolist()  # At least 25% of samples
samples_to_keep = metadata.index.values.tolist()
table_filt = table.filter(features_to_keep, axis="observation")
table_filt = table_filt.filter(common_samples, axis="sample")

# Filter metadata to match the filtered table samples
metadata = metadata[metadata.index.isin(table_filt.ids())]

print("table_filt shape:", table_filt.shape)
print("metadata shape:", metadata.shape)

# Save filtered BIOM table as a .biom file
with biom.util.biom_open("data/table-filt.biom", "w") as f:
    table_filt.to_hdf5(f, "Filtered Table")

# Save filtered metadata as a CSV file
metadata.to_csv("data/metadata-filt.tsv", sep="\t")
