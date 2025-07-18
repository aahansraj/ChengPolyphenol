import pandas as pd

# Load the dataset
df = pd.read_excel("/Users/aahansraj/Downloads/chembl_retrieve/converted_polyphenol_doses.xlsx", sheet_name="converted_clean")

# Group by compound (chembl_id) and calculate:
compound_summary = df.groupby('chembl_id').agg(
    # 1. Average activity from 'converted_value'
    average_activity=('converted_value', 'mean'),
    # 2. Count of activity data points
    activity_count=('converted_value', 'count')
).reset_index()

# Save to file
compound_summary.to_csv("compound_activity_summary.csv", index=False)
