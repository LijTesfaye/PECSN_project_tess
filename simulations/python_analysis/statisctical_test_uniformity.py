import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare

# Load your data (replace 'data.csv' with your filename)
data = pd.read_csv('../car_positions.csv')

# Group the data by CarID and then into 1-second intervals
data['TimeInterval'] = (data['SimTime'] // 1).astype(int)  # Create 1-second bins
grouped = data.groupby(['CarID', 'TimeInterval'])

# Aggregate data for each interval
aggregated_data = grouped.agg(
    mean_x=('cPositionX', 'mean'),
    mean_y=('cPositionY', 'mean'),
    std_x=('cPositionX', 'std'),
    std_y=('cPositionY', 'std'),
    count=('SimTime', 'count')  # Number of data points in the interval
).reset_index()

# Analyze uniformity by inspecting the variance
uniformity_analysis = aggregated_data.groupby('CarID').agg(
    var_x=('mean_x', 'var'),
    var_y=('mean_y', 'var'),
    mean_points=('count', 'mean')  # Average number of points per interval
).reset_index()


# Chi-Square test for uniformity
chisquare_results = []
for car_id, car_data in aggregated_data.groupby('CarID'):
    observed_x = car_data['mean_x'].values
    observed_y = car_data['mean_y'].values

    # Normalize observed frequencies for comparison to uniform distribution
    bins_x = np.histogram_bin_edges(observed_x, bins='auto')
    bins_y = np.histogram_bin_edges(observed_y, bins='auto')

    hist_x, _ = np.histogram(observed_x, bins=bins_x)
    hist_y, _ = np.histogram(observed_y, bins=bins_y)

    # Scale expected frequencies to match the sum of observed frequencies
    expected_x = np.full_like(hist_x, fill_value=hist_x.sum() / len(hist_x))
    expected_y = np.full_like(hist_y, fill_value=hist_y.sum() / len(hist_y))

    # Adjust expected frequencies to match observed sums
    expected_x = expected_x * (hist_x.sum() / expected_x.sum())
    expected_y = expected_y * (hist_y.sum() / expected_y.sum())

    chi2_x, p_x = chisquare(hist_x, expected_x)
    chi2_y, p_y = chisquare(hist_y, expected_y)

    chisquare_results.append({
        'CarID': car_id,
        'Chi2_X': chi2_x,
        'P_X': p_x,
        'Chi2_Y': chi2_y,
        'P_Y': p_y
    })
    
chisquare_df = pd.DataFrame(chisquare_results)

# Plot histograms for variance
plt.figure(figsize=(12, 6))

# Histogram for var_x
plt.subplot(1, 2, 1)
plt.hist(uniformity_analysis['var_x'], bins=20, color='blue', alpha=0.7, edgecolor='black')
plt.title('Variance in Mean X Positions Across Intervals')
plt.xlabel('Variance (X)')
plt.ylabel('Frequency')

# Histogram for var_y
plt.subplot(1, 2, 2)
plt.hist(uniformity_analysis['var_y'], bins=20, color='green', alpha=0.7, edgecolor='black')
plt.title('Variance in Mean Y Positions Across Intervals')
plt.xlabel('Variance (Y)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Display results
print("Aggregated Data (1-second intervals):")
print(aggregated_data.head())

print("\nUniformity Analysis:")
print(uniformity_analysis)

print("\nChi-Square Test Results:")
print(chisquare_df)

