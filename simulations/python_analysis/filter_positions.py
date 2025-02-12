import pandas as pd
import numpy as np

# Load CSV file
df = pd.read_csv("../car_positions.csv", names=["SimTime", "CarID", "PositionX", "PositionY"])

# Convert PositionX and PositionY to numeric, forcing errors to NaN
df["PositionX"] = pd.to_numeric(df["PositionX"], errors='coerce')
df["PositionY"] = pd.to_numeric(df["PositionY"], errors='coerce')

# Drop rows with NaN values in PositionX or PositionY
df = df.dropna(subset=["PositionX", "PositionY"])

# Get min and max values for x and y
min_x, max_x = df["PositionX"].min(), df["PositionX"].max()
min_y, max_y = df["PositionY"].min(), df["PositionY"].max()

# Define a threshold to remove values near the min and max (e.g., 10% of the range)
threshold_x = (max_x - min_x) * 0.1
threshold_y = (max_y - min_y) * 0.1

# Filter rows that are too close to the min and max values
filtered_df = df[(df["PositionX"] > (min_x + threshold_x)) & (df["PositionX"] < (max_x - threshold_x)) & 
                 (df["PositionY"] > (min_y + threshold_y)) & (df["PositionY"] < (max_y - threshold_y))]

# Optional: If you want to sample uniformly from the filtered data
# For example, you can select 100 random entries
uniform_sampled_df = filtered_df.sample(n=100, random_state=42)

# Save the filtered (and optionally sampled) data to a new CSV
uniform_sampled_df.to_csv("filtered_positions.csv", index=False)

print(f"Filtered data saved to 'filtered_positions.csv'.")

