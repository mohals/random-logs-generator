# random-logs-generator
Python synthetic log data generator for data training purposes

Outage Simulation:

Simulate 1 outage per month.
Simulate 2 outages in 1 random month.
Outages will be distributed across different apps and APIs.
Data Fields:

---Data Fields---

General:

Timestamp
App name
API name
Resource Utilization:

CPU usage (%)
Memory usage (%)
Network bandwidth (KB/s)
Response Metrics:

Response time (ms)
Error code
Additional Fields:

User ID (optional)
Request size (bytes)
Response size (bytes)
Making Data Real:

Fluctuations: Implement functions to generate realistic fluctuations in resource utilization and response times.
Anomalies: Simulate sudden spikes/dips in metrics during outages.
Seasonal trends: Incorporate seasonal variations in resource usage and request patterns.
Event-based anomalies: Optionally, include simulated events like software updates or hardware upgrades impacting performance.
