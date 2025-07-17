import pandas as pd

# Read the TSV file with tab separator and no quoting
df = pd.read_csv("poly_out_id.tsv", sep="\t", quoting=3, header=0, engine="python")

# Optional cleanup (if needed):
df["inchikey"] = df["inchikey"].str.strip('"')
df["assay_description"] = df["assay_description"].str.strip('"')

# Save the cleaned output
df.to_csv("cleaned_poly_out_id.tsv", sep="\t", index=False)
