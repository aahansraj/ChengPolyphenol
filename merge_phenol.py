import pandas as pd

# Load the two CSV files
file1 = "/Users/aahansraj/Downloads/phenol_explorer_smiles_filtered.csv"
file2 = "/Users/aahansraj/Downloads/phenol_explorer_compounds_filtered.csv"

df_smiles = pd.read_csv(file1)
df_compounds = pd.read_csv(file2)

# Merge using df_compounds as the base
merged_df = pd.merge(df_compounds, df_smiles, on='id', how='left', suffixes=('_compound', '_smiles'))

# Process overlapping columns
for col in df_smiles.columns:
    if col != 'id':  # skip join key
        col_comp = col + '_compound'
        col_smiles = col + '_smiles'
        if col_comp in merged_df.columns and col_smiles in merged_df.columns:
            # Create a new unified column
            def resolve_row(comp_val, smiles_val):
                if pd.isna(comp_val):
                    return smiles_val
                if pd.isna(smiles_val):
                    return comp_val
                if str(comp_val).strip() == str(smiles_val).strip():
                    return comp_val
                return f"{comp_val}; {smiles_val}"

            merged_df[col] = merged_df.apply(lambda row: resolve_row(row[col_comp], row[col_smiles]), axis=1)

            # Drop original suffix columns
            merged_df.drop(columns=[col_comp, col_smiles], inplace=True)

# Save cleaned merged DataFrame
output_path = "/Users/aahansraj/Downloads/merged_data_updated.csv"
merged_df.to_csv(output_path, index=False)

print("Cleaned merged file saved to:", output_path)
