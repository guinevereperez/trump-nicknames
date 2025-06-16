# -*- coding: utf-8 -*-
import os
import pandas as pd

# Folder containing individual nickname CSVs
data_folder = "data"

# List of CSVs to merge
csv_files = [
    "nicknames_wiki.csv",
    "nicknames_media.csv",
    "nicknames_reddit.csv"
]

merged_df = pd.DataFrame()

for filename in csv_files:
    path = os.path.join(data_folder, filename)
    if os.path.exists(path):
        print("✅ Merging:", filename)
        df = pd.read_csv(path)
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    else:
        print("⚠️ Skipping missing file:", filename)

# Remove duplicates based on nickname + source
merged_df.drop_duplicates(subset=["Nickname", "Specific Source Name"], inplace=True)

# Save merged output
output_path = os.path.join(data_folder, "nicknames_master.csv")
merged_df.to_csv(output_path, index=False)

print("\n✅ Saved master file to:", output_path)
print("🔢 Total nicknames:", len(merged_df))

