import pandas as pd

# Load your CSV
df = pd.read_csv("/Users/aahansraj/Downloads/merged_with_source.csv")

# Function to merge non-null values in a group
def merge_group(group):
    combined = {}
    for col in group.columns:
        if col == "name":
            combined[col] = group.iloc[0][col]
        else:
            # Drop NA, convert to string, deduplicate, and join
            values = group[col].dropna().astype(str).unique()
            combined[col] = "; ".join(values)
    return pd.Series(combined)

# Group by 'name' and apply merging
df_combined = df.groupby("name", as_index=False).apply(merge_group)

# Save to new CSV
df_combined.to_csv("/Users/aahansraj/Downloads/merged_data_final_updated.csv", index=False)
print("Concatenated file saved as 'merged_by_name.csv'")
