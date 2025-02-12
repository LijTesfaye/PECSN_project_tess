import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Define the folder containing results
test_folders = ["../sensingResults/warmupTime_Test"]
simtime_limit = 60000
fallback_warmupTime = 0.15 * simtime_limit  # 15% of total simulation time
print("Fallback Warm-up Time:", fallback_warmupTime)

# Get all CSV files
csv_files = glob.glob(f"{test_folders[0]}/*.csv")

if not csv_files:
    print(f"No CSV files found in {test_folders}.")
    exit()

plt.figure(figsize=(12, 6))  # Setup figure size
all_data = []  # Store processed data

for file in csv_files:
    print(f"Processing: {file}")
    try:
        # Read file
        data = pd.read_csv(file, on_bad_lines='skip', header=0)

        # Ensure required columns exist
        expected_columns = ["SimulationTime", "runNumber", "CarID", "count", "rate"]
        if not all(col in data.columns for col in expected_columns):
            print(f"Fixing {file}: Incorrect headers.")

            # Try to fix headers
            data = pd.read_csv(file, on_bad_lines='skip', header=None)
            if data.shape[1] == len(expected_columns):
                data.columns = expected_columns
                data.to_csv(file, index=False)  # Overwrite with corrected headers
                print(f"Rewritten {file} with correct headers.")
            else:
                print(f"Skipping {file}: Invalid format.")
                continue
        
        # Extract relevant columns
        df = data[["SimulationTime", "rate"]].sort_values("SimulationTime")

        # Aggregate rates over the same SimulationTime
        df_grouped = df.groupby("SimulationTime")["rate"].sum()

        # Convert index to numeric
        df_grouped.index = pd.to_numeric(df_grouped.index, errors='coerce')

        # Store data
        all_data.append(df_grouped)

        # **Overlay each run on the plot**
        plt.plot(df_grouped.index, df_grouped.values, alpha=0.3, label=file.split("/")[-1])  

    except Exception as e:
        print(f"Error processing {file}: {e}")
        continue

# Plot formatting
plt.xlabel("Simulation Time")
plt.ylabel("Sensing Rate")
plt.title("Time Series of Sensing Rate Across 45 Runs")
plt.legend([], [], frameon=False)  # Hide legend for clarity
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()



