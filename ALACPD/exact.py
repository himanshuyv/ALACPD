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
    llr = np.log(sigma0 / sigma1) + ((data - mu0)**2 / (2 * sigma0**2)) - ((data - mu1)**2 / (2 * sigma1**2))
    plt.plot(llr)
    plt.title("LLR Values")
    plt.show()

    
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
file_path = "./datasets/std/data_std.txt"
with open(file_path, "r") as f:
    lines = f.readlines()
    mean1 = int(lines[0].split(" ")[1][:-1])
    scale1 = float(lines[0].split(" ")[3][:-1])
    mean2 = int(lines[1].split(" ")[1][:-1])
    scale2 = float(lines[1].split(" ")[3][:-1])
    lines = lines[2:]
    data = [float(x[:-1]) for x in lines]

print(mean1, scale1, mean2, scale2)

data = np.asarray(data)
print(data[0])

# Parameters
mu0, sigma0 = mean1, scale1  # Pre-change distribution
mu1, sigma1 = mean2, scale2  # Post-change distribution
h = 5  # Detection threshold

# Run CUSUM
change_detected, S_values = exact_cusum(data, mu0, sigma0, mu1, sigma1, h)
print(change_detected)

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
plt.savefig("./exact_fig/mean1="+str(mean1)+"_scale1="+str(scale1)+"_mean2="+str(mean2)+"_scale2="+str(scale2)+".png")