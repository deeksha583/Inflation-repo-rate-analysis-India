import pandas as pd
import numpy as np

# Read the merged data
data = pd.read_csv('inflation_repo_dataset.csv')
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values('Date')

# Repo_Rate already in percentage; CPI column now holds inflation percentage


# Write results to file
with open('trend_analysis_results.txt', 'w') as f:
    f.write("=== TREND ANALYSIS: INFLATION vs REPO RATE ===\n\n")
    
    # Overall correlation
    correlation = data['CPI'].corr(data['Repo_Rate'])
    f.write(f"Overall Correlation between CPI and Repo Rate: {correlation:.3f}\n")
    f.write("(+1 = perfect positive, 0 = no correlation, -1 = perfect negative)\n\n")
    
    # Year-over-year changes
    data['Year'] = data['Date'].dt.year
    yearly_data = data.groupby('Year').agg({'CPI': 'mean', 'Repo_Rate': 'mean'})
    yearly_data['CPI_change'] = yearly_data['CPI'].pct_change() * 100
    yearly_data['Repo_change'] = yearly_data['Repo_Rate'].pct_change() * 100
    
    f.write("Year-over-Year Trends (last 10 years):\n")
    f.write(yearly_data[['CPI', 'Repo_Rate', 'CPI_change', 'Repo_change']].tail(10).to_string())
    f.write("\n\n")
    
    # Check for lagged correlation
    f.write("Lagged Correlations (does Repo Rate follow CPI with delay?):\n")
    for lag in [1, 3, 6, 12]:
        lagged_corr = data['CPI'].corr(data['Repo_Rate'].shift(lag))
        f.write(f"  CPI vs Repo Rate lagged {lag} months: {lagged_corr:.3f}\n")
    
    f.write("\n=== KEY OBSERVATIONS ===\n")
    
    # Rising inflation periods
    inflation_surges = data[data['CPI'] > data['CPI'].quantile(0.75)]
    repo_during_surge = inflation_surges['Repo_Rate'].mean()
    overall_repo_avg = data['Repo_Rate'].mean()
    f.write(f"Avg Repo Rate during HIGH inflation periods: {repo_during_surge:.4f}\n")
    f.write(f"Avg Repo Rate overall: {overall_repo_avg:.4f}\n")
    if repo_during_surge > overall_repo_avg:
        f.write("Yes, Repo Rate is HIGHER during inflation surges\n")
    else:
        f.write("No, Repo Rate is LOWER during inflation surges\n")

print("Analysis complete!")
