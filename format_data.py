import pandas as pd

# Read the merged data
data = pd.read_csv("inflation_repo_dataset.csv")

# Select and format columns (dataset already contains inflation % in CPI)
# use the CPI column directly rather than the original Close price
clean_data = data[["Date", "Repo_Rate", "CPI"]].copy()
clean_data["Date"] = pd.to_datetime(clean_data["Date"]).dt.strftime("%b %Y")
# columns are already correctly named
# clean_data.columns = ["Date", "Repo_Rate", "CPI"]
clean_data["Repo_Rate"] = clean_data["Repo_Rate"].round(2)
clean_data["CPI"] = clean_data["CPI"].round(2)

# Save to CSV
clean_data.to_csv("inflation_repo_clean.csv", index=False)

# Print as markdown table to file
with open("inflation_repo_table.md", "w") as f:
    f.write("| Date | Repo_Rate | CPI |\n")
    f.write("|------|-----------|-----|\n")
    for idx, row in clean_data.iterrows():
        f.write(f"| {row['Date']} | {row['Repo_Rate']} | {row['CPI']} |\n")

print("Done!")
print(f"Total rows: {len(clean_data)}")
