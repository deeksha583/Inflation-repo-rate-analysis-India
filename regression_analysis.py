import pandas as pd
import statsmodels.api as sm

# Load dataset
df = pd.read_csv('inflation_repo_dataset.csv')

# Prepare variables
X = df['CPI']
X = sm.add_constant(X)
y = df['Repo_Rate']

# Fit OLS model
model = sm.OLS(y, X).fit()

# Print results
print(model.summary())

# Key metrics
print("\n" + "="*60)
print("KEY ECONOMETRIC FINDINGS")
print("="*60)
print(f"R-squared: {model.rsquared:.6f}")
print(f"Coefficient (CPI effect on Repo Rate): {model.params['CPI']:.6f}")
print(f"P-value (CPI coefficient): {model.pvalues['CPI']:.6f}")
print(f"Constant (Intercept): {model.params['const']:.6f}")
print(f"P-value (Intercept): {model.pvalues['const']:.6f}")
print("="*60)

# Interpretation
print("\nINTERPRETATION:")
if model.pvalues['CPI'] < 0.05:
    print("✅ CPI effect is STATISTICALLY SIGNIFICANT (p < 0.05)")
else:
    print("❌ CPI effect is NOT statistically significant (p >= 0.05)")

print(f"\n→ For every 1% increase in inflation (CPI),")
print(f"  repo rate increases by {model.params['CPI']:.6f} basis points")
