import glob
import numpy as np
import pandas as pd
#    
# Test folders
test_folders = [
    "../sensingResults/Theoretical_Test1",
    "../sensingResults/Theoretical_Test2",
    "../sensingResults/Theoretical_Test3",
    "../sensingResults/Theoretical_Test4"
]

# Parameters
num_cars = 10  # Total number of cars
alpha_value = 0.01  # From configuration
sim_time_limit = 2000  # Simulation time limit in seconds

communication_range = [50, 100, 150, 200]  # Varying communication ranges (in meters)
L = 500  # Length of the simulation area (in meters)
H = 500  # Height of the simulation area (in meters)
# Step 1: Calculate car density (lambda_density)
lambda_density = num_cars / (L * H)  # Cars per square meter
# Step 2: Calculate Poisson parameter (lambda_poisson) for each communication range
lambda_poisson = [lambda_density * (np.pi * r**2) for r in communication_range]

# Step 3: Calculate E[N] for each communication range
E_N_theoretical = [num_cars * lambda_p for lambda_p in lambda_poisson]

# Output theoretical results
print("Car density (lambda_density):", lambda_density)
print("Lambda (Poisson parameter):", lambda_poisson)
print("Expected number of vehicles sensed (E[N]):", E_N_theoretical)


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


def calculate_e_n_observed_with_interval(test_folder, num_cars, sim_time_limit, alpha_value, communication_range):
    """
    Calculates the observed E[N] from the simulation results using sensing interval.
    
    Parameters:
        test_folder (str): Path to the folder containing .csv files.
        num_cars (int): Total number of cars in the simulation.
        sim_time_limit (float): Total simulation time limit (seconds).
        alpha_value (float): Alpha value for sensing interval calculation.
        communication_range (float): Communication range (meters).
    
    Returns:
        float: Observed E[N].
    """

    csv_files = glob.glob(f"{test_folder}/*.csv")
    if not csv_files:
        print(f"No CSV files found in {test_folder}.")
        return np.nan
    
    total_count = 0

    for file in csv_files:
        data = pd.read_csv(file, on_bad_lines='skip')
        if 'count' not in data.columns:
            print(f"'count' column missing in file: {file}")
            continue
        
        total_count += data['count'].sum()  # Sum up all counts across all events

    # Calculate sensing interval and total events
    sensing_interval = alpha_value * (communication_range ** 2)
    total_events = sim_time_limit / sensing_interval
    print("total_events",total_events)
    if total_events == 0:
        print(f"No valid sensing events for folder {test_folder}.")
        return np.nan
    
    # Calculate observed E[N]
    e_n_observed = total_count / (num_cars * total_events)
    e_n_observed2 = total_count / (num_cars)
    return {e_n_observed, e_n_observed2}

#
# Calculate theoretical E[N]
lambda_density = num_cars / (L * H)
E_N_theoretical = [
    num_cars * lambda_density * (np.pi * r**2) for r in communication_range
]

# Collect data for plotting
means_list = []
std_list = []
CI_list = []

for folder in test_folders:
    mean, std, size = calculate_mean_std(folder)
    print(f"Folder: {folder}, Mean: {mean}, Std: {std}, Sample Size: {size}")
    means_list.append(mean)
    std_list.append(std)
    #CI_list.append(calculate_confidence_interval(0.05, std, size))  # 95% CI


print("means_list: ",means_list)
# Calculate observed E[N] and compare
for i, folder in enumerate(test_folders):
    e_n_observed,e_n_observed2 = calculate_e_n_observed_with_interval( folder,
                                                         num_cars,
                                                         sim_time_limit,
                                                         alpha_value,
                                                         communication_range[i]
                                                         )
    
    #
    print(f"Test {i + 1}:")
    print(f"  Theoretical E[N]: {E_N_theoretical[i]:.2f}")
    print(f"  Observed E[N]: {e_n_observed:.2f}")
    print(f"  Observed2 E[N]: {e_n_observed2:.2f}")
    print(f"  Difference: {abs(E_N_theoretical[i] - e_n_observed):.2f}")   
    print(f"  Difference2: {abs(E_N_theoretical[i] - e_n_observed2):.2f}")
    
    
    
