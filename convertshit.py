import pandas as pd

# Explicitly specify openpyxl
file_path = "data/Cleaned_Cancer_Data.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

# Convert to JSON format
json_output_path = "data/cancer_data.json"
df.to_json(json_output_path, orient="records", indent=4)

print(f"Cleaned data saved as {json_output_path}")
