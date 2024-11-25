from statsmodels.stats.power import TTestIndPower

# Parameters for power analysis
effect_size = 0.5  # Medium effect size (adjust as needed based on your study)
alpha = 0.05       # Significance level
power = 0.8        # Desired power level (80%)

# Initialize power analysis
analysis = TTestIndPower()

# Calculate the required sample size
required_sample_size = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power, alternative='two-sided')

print(f"Required number of posts: {int(required_sample_size)}")
