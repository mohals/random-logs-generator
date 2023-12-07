import random
import time
import openpyxl
from datetime import datetime, timedelta

# Define apps and APIs
apps = ["Buy", "Market Place", "AWS Challenge", "Freeze"]
apis = ["/rewards", "/apply", "/alerts"]

# Define outage types and durations
outage_types = {
    "cpu_overload": {"duration": 10, "cpu_spike": 90},
    "memory_leak": {"duration": 20, "memory_usage": 80},
    "network_issue": {"duration": 5, "response_time": 1000},
    "software_bug": {"duration": 15, "error_rate": 0.1},
}

# Define functions to generate data
def generate_timestamp(start_date, end_date):
    delta = end_date - start_date
    return start_date + timedelta(seconds=random.randrange(int(delta.total_seconds())))

def generate_api_request(app, api, timestamp):
    return {
        "timestamp": timestamp,
        "app": app,
        "api": api,
        "response_time": random.randint(50, 200),
        "error_code": None,
        "cpu_usage": random.randint(10, 50),
        "memory_usage": random.randint(10, 50),
    }

def generate_fluctuation(value, amplitude=0.1):
    return value + random.uniform(-amplitude, amplitude) * value

def generate_anomaly(data, outage_type, timestamp):
    duration = outage_types[outage_type]["duration"]
    end_time = (timestamp + timedelta(seconds=duration)).timestamp()
    
    while end_time > generate_timestamp(start_date, end_date).timestamp():
        for key, value in outage_types[outage_type].items():
            if key not in ["duration", "type"]:
                data[key] = value
        yield data
        time.sleep(1)


# Define start and end dates
start_date = datetime(2022, 11, 1)
end_date = datetime(2023, 10, 31)

# Initialize Excel workbook
wb = openpyxl.Workbook()
ws = wb.active

# Write header row
ws.append(["Timestamp", "App", "API", "Response Time", "Error Code", "CPU Usage", "Memory Usage", "Network Bandwidth"])

# Generate data
log_data = []
current_date = start_date
month_count = 1
while current_date <= end_date:
    # Simulate outages
    outage_count = random.randint(1, 2) if month_count != 12 else 1

    for _ in range(outage_count):
        outage_type = random.choice(list(outage_types.keys()))
        outage_timestamp = generate_timestamp(current_date, current_date + timedelta(days=30))
        # Initialize a new data dictionary before calling generate_anomaly
        data = generate_api_request(random.choice(apps), random.choice(apis), outage_timestamp)
        log_data.extend(generate_anomaly(data.copy(), outage_type, outage_timestamp))

    # Generate normal data points
    for _ in range(10000):  # Adjust number of data points per month
        timestamp = generate_timestamp(current_date, current_date + timedelta(days=31))
        app = random.choice(apps)
        api = random.choice(apis)
        data = generate_api_request(app, api, timestamp)
        
        # Add realistic fluctuations
        data["response_time"] = generate_fluctuation(data["response_time"])
        data["cpu_usage"] = generate_fluctuation(data["cpu_usage"])
        data["memory_usage"] = generate_fluctuation(data["memory_usage"])
        
        log_data.append(data)

    # Update month count and date
    month_count += 1
    current_date = current_date + timedelta(days=31)

# Write data to Excel sheet
for data in log_data:
    ws.append([data["timestamp"], data["app"], data["api"], data["response_time"], data["error_code"], data["cpu_usage"], data["memory_usage"], data["network_bandwidth"]])

# Save Excel file
wb.save("synthetic_log_data_test3.xlsx")

print("Synthetic log data generated and saved to synthetic_log_data.xlsx")
