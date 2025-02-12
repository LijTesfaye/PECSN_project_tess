import pandas as pd
import matplotlib.pyplot as plt
import glob

# Define the folder containing results
test_folder = "../sensingResults/warmupTime_Test"
all_data = []
# Get all CSV files
csv_files = glob.glob(f"{test_folder}/*.csv")
#csv_files = glob.glob(f"{test_folder}/*.csv")


if not csv_files:
    print(f"No CSV files found in {test_folder}.")
    exit()


for file in csv_files:
    print(f"Processing: {file}")
    try:
        # Read CSV
        data = pd.read_csv(file, on_bad_lines='skip', header=0,dtype={'SimulationTime': str, 'rate': str})
        data["SimulationTime"] = pd.to_numeric(data["SimulationTime"], errors='coerce')
        data["rate"] = pd.to_numeric(data["rate"], errors='coerce')

        data = data.dropna(subset=["SimulationTime", "rate"])
        # Ensure required columns exist
        if "SimulationTime" not in data.columns or "rate" not in data.columns:
            print(f"Skipping {file}: Missing required columns.")
            continue

        # Aggregate rates by SimulationTime (sum them up)
        df_grouped = data.groupby("SimulationTime")["rate"].sum()
        
        all_data.append((df_grouped, file))  # **FIXED: Store data**

        # Plot each file's data as a separate line
        #plt.plot(df_grouped.index, df_grouped.values, label=file.split('/')[-1])
    
    except Exception as e:
        print(f"Error processing {file}: {e}")
        continue
plt.figure(figsize=(12, 6))  # Set figure size

for df_grouped, file in all_data:
    plt.plot(df_grouped.index, df_grouped.values, label=str(file.split('/')[-1]))
    print("df_grouped.index, df_grouped.values",df_grouped.index, df_grouped.values)
# Customize plot
plt.xlabel("Simulation Time")
plt.ylabel("Sum of Sensing Rates")
plt.title("Convergence Check of Sensing Rate Over Time")
plt.legend(loc="upper right", fontsize="small")  # Add legend
plt.grid(True)
plt.show()
