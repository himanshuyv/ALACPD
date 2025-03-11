import json
import numpy as np
from datetime import datetime, timedelta

# Load the original JSON file
file_path = "./../run_log/run_log.json"
with open(file_path, "r") as f:
    data = json.load(f)

# Extract required metadata
n_obs = 200
n_dim = 1
start_time = datetime.now()  # Set current timestamp as start time
time_interval = timedelta(seconds=5)

# Generate new timestamps with the current time as reference
new_timestamps = [(start_time + i * time_interval).strftime("%Y-%m-%d %H:%M:%S") for i in range(n_obs)]

# Define change points
change_points = [np.random.randint(50, 180)]

print(change_points)

curmean = np.random.randint(-20, 20)
scale1 = np.random.random()
scale2 = np.random.random()
# Generate dummy data with normal distribution
pace_data = np.random.normal(loc= curmean, scale= scale1, size=n_obs)

# Apply significant changes in distributions at specific indices
gap = np.random.randint(2, 10)
for idx in change_points:
    pace_data[idx:] = np.random.normal(loc=curmean+gap, scale=scale2, size=n_obs - idx)
# Construct the new JSON structure
new_data = {
    "name": "std",
    "longname": "Run Log",
    "n_obs": n_obs,
    "n_dim": n_dim,
    "time": {
        "type": "string",
        "format": "%Y-%m-%d %H:%M:%S",
        "index": list(range(n_obs)),
        "raw": new_timestamps,
    },
    "series": [
        {
            "label": "Pace",
            "type": "float",
            "raw": pace_data.tolist(),
        }
    ],
}

# Save the new JSON file
output_path = "std.json"
with open(output_path, "w") as f:
    json.dump(new_data, f, indent=4)

with open("data_std.txt", "w") as f:
    mean1 = curmean
    mean2 = curmean+gap
    f.write(f"Mean1: {mean1}, Scale1: {scale1}\n")
    f.write(f"Mean2: {mean2}, Scale2: {scale2}\n")
    np.savetxt(f, pace_data, fmt='%.6f', delimiter=',')
