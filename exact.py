import numpy as np
import matplotlib.pyplot as plt

def exact_cusum(data, mu0, sigma0, mu1, sigma1, h):
    """
    Implements the Exact CUSUM method for change point detection.
    
    Parameters:
    data  : numpy array, sequence of observations
    mu0   : float, mean of pre-change distribution
    sigma0: float, std deviation of pre-change distribution
    mu1   : float, mean of post-change distribution
    sigma1: float, std deviation of post-change distribution
    h     : float, threshold for detection
    
    Returns:
    change_point: int, index where change is detected (or None if no change detected)
    S_values    : list, CUSUM statistic values over time
    """
    # Compute log-likelihood ratio
    llr = np.log(sigma0 / sigma1) + (sigma0**2 + (data - mu0)**2) / (2 * sigma0**2) - (sigma1**2 + (data - mu1)**2) / (2 * sigma1**2)
    
    S = 0
    S_values = []
    change_point = None
    
    for t in range(len(data)):
        S = max(0, S + llr[t])  # CUSUM update
        S_values.append(S)
        if S > h:
            change_point = t
            break
    
    return change_point, S_values

# Simulated Data
np.random.seed(42)
data_pre = np.random.normal(-11, 0.185, 100)    # Pre-change samples
change_point_true = 100
data_post = np.random.normal(-20, 0.023, 100)   # Post-change samples

data = np.concatenate([data_pre, data_post])
print(data)
# Parameters
mu0, sigma0 = -11, 0.185  # Pre-change distribution
mu1, sigma1 = -20, 0.023  # Post-change distribution
h = 5  # Detection threshold

# Run CUSUM
change_detected, S_values = exact_cusum(data, mu0, sigma0, mu1, sigma1, h)

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(S_values, label="CUSUM Statistic", color='b')
plt.axhline(h, color='r', linestyle='--', label="Threshold")
if change_detected is not None:
    plt.axvline(change_detected, color='g', linestyle='--', label=f"Detected Change at t={change_detected}")
plt.legend()
plt.xlabel("Time")
plt.ylabel("CUSUM Statistic")
plt.title("Exact CUSUM Change Detection")
plt.show()
