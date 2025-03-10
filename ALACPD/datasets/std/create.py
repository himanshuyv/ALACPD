import json
import numpy as np
from datetime import datetime, timedelta

# Load the original JSON file
file_path = "./../run_log/run_log.json"
with open(file_path, "r") as f:
    data = json.load(f)

# Extract required metadata
n_obs = data["n_obs"]
n_dim = data["n_dim"]
start_time = datetime.now()  # Set current timestamp as start time
time_interval = timedelta(seconds=5)

# Generate new timestamps with the current time as reference
new_timestamps = [(start_time + i * time_interval).strftime("%Y-%m-%d %H:%M:%S") for i in range(n_obs)]

# Define change points
change_points = [60, 96, 114, 177, 204, 240, 258, 317]

# Generate dummy data with normal distribution
pace_data = np.random.normal(loc=15, scale=0.1, size=n_obs)

# Apply significant changes in distributions at specific indices
curmean = 15
for idx in change_points:
    pace_data[idx:] = np.random.normal(loc=curmean-5, scale=0.1, size=n_obs - idx)
    curmean -= 5

# Construct the new JSON structure
new_data = {
    "name": "std",
    "longname": "Run Log",
    "n_obs": n_obs,
    "n_dim": n_dim-1,
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
