import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
#
# Load the CSV file containing the positions
df = pd.read_csv('../car_positions.csv')
#
# Extract position coordinates

#Using current positions columns.
x_cPos_coords = df['cPositionX'] #PositionX
y_cPos_coords = df['cPositionY'] #PositionY  
# X-axis histogram, cPos
plt.subplot(1, 2, 1)
plt.hist(x_cPos_coords, bins=20, edgecolor='black', alpha=0.7)
plt.title('Histogram of X cPositions')
plt.xlabel('PositionX')
plt.ylabel('Frequency')

# Y-axis histogram, cPos
plt.subplot(1, 2, 2)
plt.hist(y_cPos_coords, bins=20, edgecolor='black', alpha=0.7)
plt.title('Histogram of Y cPositions')
plt.xlabel('PositionY')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

x_bins = np.linspace(min(x_cPos_coords), max(x_cPos_coords), 5)  # Define bin edges for X
y_bins = np.linspace(min(y_cPos_coords), max(y_cPos_coords), 5)  # Define bin edges for Y
#
# Create a 2D histogram of the positions
hist, xedges, yedges = np.histogram2d(x_cPos_coords, y_cPos_coords, bins=[x_bins, y_bins])

# Perform Chi-square test (comparing observed vs expected values)
expected_freq = np.ones_like(hist) * np.mean(hist)  # Assuming uniform distribution
chi2_stat, p_val = chisquare(hist.flatten(), expected_freq.flatten())

print(f'Chi-square statistic: {chi2_stat}')
print(f'p-value: {p_val}')

# Interpretation
if p_val < 0.05:
    print("The cPositions are not uniformly distributed (reject H0).")
else:
    print("The cPositions are uniformly distributed (fail to reject H0).")
    
##
#
#Using target positions columns.
x_tPos_coords = df['tPositionX'] #PositionX
y_tPos_coords = df['tPositionY'] #PositionY  
# X-axis histogram, tPos
plt.subplot(1, 2, 1)
plt.hist(x_tPos_coords, bins=20, edgecolor='black', alpha=0.7)
plt.title('Histogram of X tPositions')
plt.xlabel('PositionX')
plt.ylabel('Frequency')

# Y-axis histogram, tPos
plt.subplot(1, 2, 2)
plt.hist(y_tPos_coords, bins=20, edgecolor='black', alpha=0.7)
plt.title('Histogram of Y tPositions')
plt.xlabel('PositionY')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
#
x_bins = np.linspace(min(x_tPos_coords), max(y_tPos_coords), 5)  # Define bin edges for X
y_bins = np.linspace(min(y_tPos_coords), max(y_tPos_coords), 5)  # Define bin edges for Y
#
# Create a 2D histogram of the positions
hist, xedges, yedges = np.histogram2d(x_tPos_coords, y_tPos_coords, bins=[x_bins, y_bins])

# Perform Chi-square test (comparing observed vs expected values)
expected_freq = np.ones_like(hist) * np.mean(hist)  # Assuming uniform distribution
chi2_stat, p_val = chisquare(hist.flatten(), expected_freq.flatten())

print(f'Chi-square statistic: {chi2_stat}')
print(f'p-value: {p_val}')

# Interpretation
if p_val < 0.05:
    print("The tpositions are not uniformly distributed (reject H0).")
else:
    print("The tpositions are uniformly distributed (fail to reject H0).")
    
   
    