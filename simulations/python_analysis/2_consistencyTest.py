import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import glob
from scipy.stats import norm

tests_list = ["Test1", "Test2"]

def calculate_confidence_interval(alpha, std, size):
    """
    Returns the confidence interval for a population mean, using a normal distribution.
    Args:
        alpha: The significance level used to compute the confidence level.
        The confidence level equals 100*(1 - alpha)%, 
        or in other words, an alpha of 0.05 indicates a 95% confidence level.
        std: The population standard deviation for the data range and is assumed to be known.
        size: The sample size
    """
    return std * norm.ppf(1 - alpha / 2) / np.sqrt(size)



def calculate_mean_std(test_folder):
    # grab all the files in the current test folder
    csv_files = glob.glob(f"{test_folder}/*.csv")
    # Accumulate the rates of this test
    rates = []
    for file in csv_files:
        data = pd.read_csv(file, on_bad_lines='skip')
        rates.extend(data['rate'].tolist())  # Append 'rate' column values
        
    #
    mean = np.mean(rates)
    #variance = np.mean((rates - mean) ** 2)
    std = np.std(rates, ddof=1)  # Use sample std deviation (ddof=1)
    return(mean, std, len(rates))

#
test_folders = ["../sensingResults/Consistency_Test1", 
                "../sensingResults/Consistency_Test2"
                ]

# Collect data for plotting
means_list = []
std_list = []
CI_list = []

#
for folder in test_folders:
    mean, std, size = calculate_mean_std(folder)
    print("size:",size)
    means_list.append(mean)
    std_list.append(std)
    CI_list.append(calculate_confidence_interval(0.05, std, size))  # 95% CI
    
# Calculate the difference between the means
print(f"mean_list:{means_list}")
mean_difference = abs(means_list[0] - means_list[1])
print(f"Difference between means: {mean_difference:.4f}")

#
# Plot the bar graph with error bars
colors = ['green', 'orange']  # Colors for Test1 and Test2
plt.figure(figsize=(10, 6))
plt.bar(tests_list, means_list, yerr=CI_list, capsize=10, color=colors, alpha=0.8)
plt.xlabel("TESTS", fontsize=12)
plt.ylabel("Mean Sensing Rate", fontsize=14)
plt.title("Consistency Test (with 95% CI)", fontsize=14)
plt.xticks(tests_list)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("consistencyTest_with_95ci.png", dpi=300)
plt.show()

    