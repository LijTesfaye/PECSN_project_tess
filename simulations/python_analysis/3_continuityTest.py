import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import glob
from scipy.stats import norm

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
test_folders = ["../sensingResults/Continuity_Test1", 
                "../sensingResults/Continuity_Test2", 
                "../sensingResults/Continuity_Test3"]


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

#
# Plot the bar graph with error bars
tests_list = ["Test1(numCars=20)", "Test2(numCars=21)", "Test3(numCars=22)"]
colors = ['blue', 'orange', 'green']
plt.figure(figsize=(10, 6))
plt.bar(tests_list, means_list, yerr=CI_list, capsize=10, color=colors, alpha=0.8)

plt.xlabel("Number of Cars", fontsize=12)
plt.ylabel("Mean Sensing Rate", fontsize=12)
plt.title("Continuity Test (with 95% CI)", fontsize=14)
plt.xticks(tests_list)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

#plt.legend(bars, tests_list, title="Configurations", loc="upper left")
plt.savefig("continuityTest_with_95ci.png", dpi=300)
plt.show()

"""
This part is very important.
"""
# Analyze non-monotonicity
print("Checking for non-monotonicity:")
for i in range(1, len(means_list)):
    print(f"mean difference {abs(means_list[i] -means_list[i - 1])}")
    if means_list[i] < means_list[i - 1]:
        print(f"Non-monotonic behavior detected: {tests_list[i]} < {tests_list[i-1]}")
    else:
        print(f"Non-monotonic behavior  is NOT detected.")
#
print(f"Mean list:- {means_list}")

