import json
import numpy as np
from datetime import datetime, timedelta

# Load the original JSON file
file_path = "./../run_log/run_log.json"
with open(file_path, "r") as f:
    data = json.load(f)

n_obs = 300
n_dim = 1
start_time = datetime.now()
time_interval = timedelta(seconds=5)

new_timestamps = [(start_time + i * time_interval).strftime("%Y-%m-%d %H:%M:%S") for i in range(n_obs)]

change_points = [60, 110, 190, 250]

# Generate dummy data with Bernoulli distribution
# Initial probability for success (i.e., value 1)
p_values = [0.9, 0.5, 0.8, 0.3, 0.7] 
x_data = np.random.binomial(n=1, p=p_values[0], size=n_obs)
for i in range(1, len(change_points)):
    x_data[change_points[i-1]:change_points[i]] = np.random.binomial(n=1, p=p_values[i], size=change_points[i] - change_points[i-1])

new_data = {
    "name": "bernoulli",
    "longname": "Bernoulli Distribution",
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
            "label": "x",
            "type": "float",
            "raw": x_data.tolist(),
        }
    ],
}

# Save the new JSON file
output_path = "bernoulli.json"
with open(output_path, "w") as f:
    json.dump(new_data, f, indent=4)
