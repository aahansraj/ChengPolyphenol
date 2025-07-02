import pandas as pd

# Load datasets
phenol_df = pd.read_csv("/Users/aahansraj/Downloads/merged_data_updated.csv")
phytohub_df = pd.read_csv("/Users/aahansraj/Downloads/phytohub_compounds_filtered.csv")

# Standardize SMILES column name
phytohub_df = phytohub_df.rename(columns={"Smiles": "smiles"})

# Add source flags before merging
phenol_df["source_phenol"] = True
phytohub_df["source_phytohub"] = True

# Merge datasets on 'smiles'
merged = pd.merge(
    phenol_df,
    phytohub_df,
    on="smiles",
    how="outer",
    suffixes=("_phenol", "_phytohub")
)

# Fill missing source flags
merged["source_phenol"] = merged["source_phenol"].fillna(False)
merged["source_phytohub"] = merged["source_phytohub"].fillna(False)

# Create a unified source label
def determine_source(row):
    if row["source_phenol"] and row["source_phytohub"]:
        return "Both"
    elif row["source_phenol"]:
        return "Phenol Explorer"
    elif row["source_phytohub"]:
        return "PhytoHub"
    else:
        return "Unknown"

merged["source"] = merged.apply(determine_source, axis=1)

# Merge overlapping columns
# Name
merged["name"] = merged["name"].combine_first(merged["Chemical Name"])
# Class
merged["compound_class"] = merged["compound_class"].combine_first(merged["Phytochemical class"])
# Subclass
merged["compound_subclass"] = merged["compound_subclass"].combine_first(merged["Phytochemical subclass"])
# Synonyms
merged["synonyms"] = merged["synonyms"].fillna("") + "; " + merged["Synonyms"].fillna("")
merged["synonyms"] = merged["synonyms"].str.strip("; ").str.strip()
# CAS number
merged["cas_number"] = merged["cas_number"].combine_first(merged["CAS Number"])

# Drop duplicate or now-merged columns
columns_to_drop = [
    "Chemical Name",
    "Phytochemical class",
    "Phytochemical subclass",
    "Synonyms",
    "CAS Number",
    "source_phenol",
    "source_phytohub"
]
merged.drop(columns=[col for col in columns_to_drop if col in merged.columns], inplace=True)

# Save the result
merged.to_csv("/Users/aahansraj/Downloads/merged_with_source.csv", index=False)
