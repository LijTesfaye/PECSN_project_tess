import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#
# Directory containing the CSV files.
folder_path = "../sensingResults/overAllRate"
numCars = 10
# Directory containing the CSV files

# Initialize storage for alpha, M, and overallSensingRate
data = {}

if not os.path.exists(folder_path):
    raise FileNotFoundError(f"Folder '{folder_path}' does not exist.")

#
# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.startswith("vehicles_sensed") and file_name.endswith(".csv"):
        try:
            # Extract alpha and M from the file name using specific keywords
            parts = file_name.split("_")
            alpha = float(parts[3])  # Third part is alpha
            M = int(parts[4].split(".")[0])  # Fourth part is M (removing .csv)

            # Read the CSV file and calculate the overall sensing rate
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path,on_bad_lines='skip')
            
            if "rate" not in df.columns:
                print(f"Skipping file {file_name}: '{'rate'}' column not found.")
                continue
            
            df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
            
            #df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
            # Sum the rate column to get the overall sensing rate for this file
            overall_sensing_rate = df["rate"].sum()
            # Normalize the sensing rate by all the cars in the simulation
            overall_sensing_rate = overall_sensing_rate/numCars
            # Aggregate results for the same alpha and M combination
            if (alpha, M) not in data:
                data[(alpha, M)] = overall_sensing_rate
            else:
                data[(alpha, M)] += overall_sensing_rate

        except ValueError as e:
            print(f"Skipping file {file_name} due to parsing error: {e}")

print("data ",data)

# Convert collected data to a DataFrame for easier manipulation
df_result = pd.DataFrame(
    [(alpha, M, overall_rate) for (alpha, M), overall_rate in data.items()],
    columns=["Alpha", "M", "OverallSensingRate"]
)

# Create a pivot table for heatmap visualization
pivot_table = df_result.pivot(index="M", columns="Alpha", values="OverallSensingRate")

# Plot the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(
    pivot_table,
    annot=True,  # Show values in cells
    fmt=".2f",   # Format for values
    cmap="YlGnBu",  # Colormap
    cbar_kws={"label": "OverallSensingRate"}  # Colorbar label
)
#
# Add labels and title
plt.xlabel("Alpha (α)", fontsize=12)
plt.ylabel("Transmission Range (M)", fontsize=12)
plt.title("Effect of Alpha and M on Overall Sensing Rate", fontsize=14)
#
plt.savefig("heatmap_overall_sensing_rate.png", dpi=300)

# Show the plot
plt.tight_layout()
plt.show()


