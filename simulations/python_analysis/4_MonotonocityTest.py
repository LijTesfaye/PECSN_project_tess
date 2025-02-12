import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from scipy.stats import norm

# Test configurations
tests_list = ["M(50m)", "M(100m)", "M(150m)", "M(200m)"]
colors = ['blue', 'orange', 'green', 'red']
# Test folder paths
test_folders = [
    "../sensingResults/Monotonocity_Test1",
    "../sensingResults/Monotonocity_Test2",
    "../sensingResults/Monotonocity_Test3",
    "../sensingResults/Monotonocity_Test4"
]

def calculate_confidence_interval(alpha, std, size):
    """
    Returns the confidence interval for a population mean, using a normal distribution.
    """
    if size <= 1:
        return 0  # No confidence interval for insufficient data
    return std * norm.ppf(1 - alpha / 2) / np.sqrt(size)

def calculate_mean_std(test_folder):
    """
    Calculates the mean sensing rate, standard deviation, and sample size for a test configuration.
    """
    csv_files = glob.glob(f"{test_folder}/*.csv")
    if not csv_files:
        print(f"No CSV files found in {test_folder}.")
        return np.nan, np.nan, 0

    rates = []
    for file in csv_files:
        data = pd.read_csv(file, on_bad_lines='skip')
        if 'rate' not in data.columns:
            print(f"'rate' column missing in file: {file}")
            continue
        rates.extend(data['rate'].dropna().tolist())  # Drop NaN values

    if not rates:
        print(f"No valid 'rate' data in {test_folder}.")
        return np.nan, np.nan, 0

    mean = np.mean(rates)
    std = np.std(rates, ddof=1)  # Use sample std deviation (ddof=1)
    return mean, std, len(rates)

# Collect data for plotting
means_list = []
std_list = []
CI_list = []

for folder in test_folders:
    mean, std, size = calculate_mean_std(folder)
    print(f"Folder: {folder}, Mean: {mean}, Std: {std}, Sample Size: {size}")
    means_list.append(mean)
    std_list.append(std)
    CI_list.append(calculate_confidence_interval(0.05, std, size))  # 95% CI


# Check if all data is valid
if any(np.isnan(means_list)):
    print("Error: Some configurations have invalid data. Please check the CSV files.")
else:
    # Plot the bar graph with error bars
    plt.figure(figsize=(10, 6))
    plt.bar(tests_list, means_list, yerr=CI_list, capsize=10, color=colors, alpha=0.8)
    plt.xlabel("TESTS", fontsize=12)
    plt.ylabel("Mean Sensing Rate", fontsize=14)
    plt.title("Monotonocity Test (with 95% CI)", fontsize=14)
    plt.xticks(tests_list)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("monotonicityTest_with_95ci.png", dpi=300)
    plt.show()
