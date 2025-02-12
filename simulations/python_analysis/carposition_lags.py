import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare

import matplotlib.pyplot as plt
import pandas as pd
#
# Load the CSV file containing the positions
df = pd.read_csv('../car_positions.csv')
#
"""
# Extract the relevant columns for plotting
current_positions_x = df['cPositionX']
current_positions_y = df['cPositionY']
target_positions_x = df['tPositionX']
target_positions_y = df['tPositionY']

# Create the plot
plt.figure(figsize=(10, 6))

# Plot current positions
plt.plot(current_positions_x, current_positions_y, 'bo-', label='Current Position', markersize=4)

# Plot target positions
plt.plot(target_positions_x, target_positions_y, 'ro-', label='Target Position', markersize=4)

# Add labels and title
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Current vs. Target Positions')

# Add a legend
plt.legend()

# Show the plot
plt.show()
"""
# Shift tPositions to create a lagged version
df['lagged_tPositionX'] = df['tPositionX'].shift(1)
df['lagged_tPositionY'] = df['tPositionY'].shift(1)
# Find rows where cPositions match the lagged tPositions
matching_rows = df[(df['cPositionX'] == df['lagged_tPositionX']) & (df['cPositionY'] == df['lagged_tPositionY'])]
#
plt.scatter(matching_rows['lagged_tPositionX'], matching_rows['lagged_tPositionY'], color='blue', label='Lagged tPositions')
plt.scatter(matching_rows['cPositionX'], matching_rows['cPositionY'], color='red', label='Matching cPositions', alpha=0.5)
plt.legend()
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Matching Rows: cPositions vs Lagged tPositions')
plt.show()
# Display the matching rows
print("Rows where cPositions match lagged tPositions:")
print(matching_rows.head(10))  # Show the first 10 matching rows
print(matching_rows)
##
#
df['time_bin'] = (df['SimTime'] // 1).astype(int)  # Group by 1-second intervals (or adjust as needed)
aggregated_df = df.groupby(['time_bin', 'CarID']).mean().reset_index()

df['speed'] = ((df['cPositionX'].diff()**2 + df['cPositionY'].diff()**2)**0.5) / df['SimTime'].diff()
mean_speed = df['speed'].mean()
print(f"Mean Speed: {mean_speed}")
##
#
plt.scatter(df['cPositionX'], df['cPositionY'], alpha=0.5, label='cPositions')
plt.scatter(df['tPositionX'], df['tPositionY'], alpha=0.5, label='tPositions', color='red')
plt.legend()
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Spatial Distribution of Positions')
plt.show()


