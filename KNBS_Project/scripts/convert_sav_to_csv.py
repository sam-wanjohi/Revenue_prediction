import pandas as pd
import pyreadstat

# Load the SAV file
df, meta = pyreadstat.read_sav("2010_Villas_Survey_25012013.sav")

# Optional: map categorical codes to labels
for col in meta.column_names:
    if col in meta.value_labels:
        df[col] = df[col].map(meta.value_labels[col])

# Save as CSV
df.to_csv("KNBS_Villas_2010.csv", index=False)

print("CSV file created successfully!")
