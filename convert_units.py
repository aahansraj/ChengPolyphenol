import pandas as pd

# Load the TSV file
file_path = "/Users/aahansraj/Downloads/chembl_retrieve/cleaned_poly_out_id.tsv"
df = pd.read_csv(file_path, sep="\t")

# Function to normalize units
def convert_units(row):
    value = row['standard_value']
    unit = row['standard_units']
    
    try:
        if pd.isna(value) or pd.isna(unit):
            return value, unit

        unit = unit.strip().lower()

        if unit == 'nm':
            return value, 'nM'
        elif unit == 'um':
            return value * 1_000, 'nM'
        elif unit == 'mm':
            return value * 1_000_000, 'nM'
        elif unit in ['ug.ml-1', '10^2 ug/ml', '10^3ug/ml']:
            # Cannot convert to nM without molecular weight
            return value, 'ug/mL (not normalized)'
        elif unit == 'mg kg-1':
            return value, 'mg/kg/day'
        else:
            return value, f'{unit}'
    except:
        return value, 'conversion_error'

# Apply conversion to each row
df[['converted_value', 'normalized_unit']] = df.apply(convert_units, axis=1, result_type='expand')

# Optionally, save the updated DataFrame
df.to_csv("converted_polyphenol_doses.tsv", sep="\t", index=False)
