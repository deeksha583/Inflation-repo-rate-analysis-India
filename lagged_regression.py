import pandas as pd
import statsmodels.api as sm
import numpy as np

# Load dataset
data = pd.read_csv('inflation_repo_dataset.csv')
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values('Date')

# Create lagged CPI variables
data['CPI_lag1'] = data['CPI'].shift(1)
data['CPI_lag2'] = data['CPI'].shift(2)
data['CPI_lag3'] = data['CPI'].shift(3)
data['CPI_lag6'] = data['CPI'].shift(6)
data['CPI_lag12'] = data['CPI'].shift(12)

# Drop rows with NaN from lagging
data = data.dropna().reset_index(drop=True)

print(f"Sample size after lagging: {len(data)} observations")
print(f"Date range: {data['Date'].min()} to {data['Date'].max()}")

# Prepare variables for regression
X = data[['CPI', 'CPI_lag1', 'CPI_lag2', 'CPI_lag3', 'CPI_lag6', 'CPI_lag12']]
X = sm.add_constant(X)
y = data['Repo_Rate']

# Fit OLS model
model = sm.OLS(y, X).fit()

# Print results
print("\n" + "="*80)
print("LAGGED REGRESSION ANALYSIS: Does Repo Rate Respond to Past Inflation?")
print("="*80)
print(model.summary())

print("\n" + "="*80)
print("KEY ECONOMETRIC FINDINGS")
print("="*80)
print(f"R-squared: {model.rsquared:.6f}")
print(f"Adjusted R-squared: {model.rsquared_adj:.6f}")
print(f"F-statistic: {model.fvalue:.6f}")
print(f"Prob (F-statistic): {model.f_pvalue:.6f}")

print("\nCOEFFICIENT ANALYSIS:")
coefficients = model.params
pvalues = model.pvalues

for var in ['const', 'CPI', 'CPI_lag1', 'CPI_lag2', 'CPI_lag3', 'CPI_lag6', 'CPI_lag12']:
    if var in coefficients:
        coef = coefficients[var]
        pval = pvalues[var]
        sig = "✅ SIGNIFICANT" if pval < 0.05 else "❌ NOT SIGNIFICANT"
        print(f"{var:10}: {coef:>10.6f} (p={pval:.6f}) {sig}")

print("\n" + "="*80)
print("ECONOMIC INTERPRETATION")
print("="*80)

# Check if 3-month lag is significant
if 'CPI_lag3' in pvalues and pvalues['CPI_lag3'] < 0.05:
    print("✅ EVIDENCE FOUND: Repo Rate responds to inflation after 3 months!")
    print(f"   For every 1% increase in inflation 3 months ago, repo rate increases by {coefficients['CPI_lag3']:.6f} percentage points.")
else:
    print("❌ NO EVIDENCE: Repo Rate does not significantly respond to 3-month lagged inflation.")
    print("   The 3-month lag coefficient is not statistically significant.")

print(f"\nOverall model fit: {model.rsquared:.1%} of repo rate variation explained by current and lagged inflation.")
print("This suggests RBI considers multiple time horizons when setting policy.")

# Save detailed results
with open('lagged_regression_results.txt', 'w') as f:
    f.write("LAGGED REGRESSION ANALYSIS: Repo Rate vs Current and Past Inflation\n\n")
    f.write(str(model.summary()))
    f.write("\n\nKEY FINDINGS:\n")
    f.write(f"R-squared: {model.rsquared:.6f}\n")
    f.write(f"Adjusted R-squared: {model.rsquared_adj:.6f}\n")
    f.write(f"F-statistic: {model.fvalue:.6f} (p={model.f_pvalue:.6f})\n\n")

    for var in ['const', 'CPI', 'CPI_lag1', 'CPI_lag2', 'CPI_lag3', 'CPI_lag6', 'CPI_lag12']:
        if var in coefficients:
            f.write(f"{var}: {coefficients[var]:.6f} (p={pvalues[var]:.6f})\n")

    f.write("\nCONCLUSION:\n")
    if 'CPI_lag3' in pvalues and pvalues['CPI_lag3'] < 0.05:
        f.write("Repo Rate significantly responds to 3-month lagged inflation.\n")
    else:
        f.write("No significant response to 3-month lagged inflation found.\n")

print("\nDetailed results saved to 'lagged_regression_results.txt'")