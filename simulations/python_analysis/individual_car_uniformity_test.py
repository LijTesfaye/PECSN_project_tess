import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

# Load the CSV file
df = pd.read_csv('../car_positions.csv')

# Get the list of unique car IDs
car_ids = df['CarID'].unique()

# Define the floorplan boundaries (replace with your actual floorplan size)
floorplan_x = (0, 500)  # Example: width 500
floorplan_y = (0, 500)  # Example: height 500

for car_id in car_ids:
    car_data = df[df['CarID'] == car_id]  # Filter data for this car
    x_coords = car_data['PositionX']
    y_coords = car_data['PositionY']

    # Kolmogorov-Smirnov (K-S) test for uniform distribution
    uniform_x = np.random.uniform(floorplan_x[0], floorplan_x[1], len(x_coords))
    uniform_y = np.random.uniform(floorplan_y[0], floorplan_y[1], len(y_coords))

    ks_x_stat, ks_x_pval = ks_2samp(x_coords, uniform_x)
    ks_y_stat, ks_y_pval = ks_2samp(y_coords, uniform_y)

    print(f"Car {car_id} - X Uniformity p-value: {ks_x_pval:.4f}, Y Uniformity p-value: {ks_y_pval:.4f}")

    # Visualize scatter plot
    plt.figure(figsize=(6, 5))
    plt.scatter(x_coords, y_coords, alpha=0.5)
    plt.title(f"Scatter Plot for {car_id}")
    plt.xlabel("PositionX")
    plt.ylabel("PositionY")
    plt.xlim(floorplan_x)
    plt.ylim(floorplan_y)
    plt.grid()
    plt.show()

    # Interpretation
    if ks_x_pval < 0.05 or ks_y_pval < 0.05:
        print(f"Car {car_id}'s movement is NOT uniformly distributed.")
    else:
        print(f"Car {car_id}'s movement appears uniformly distributed.")
