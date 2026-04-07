# Section 4: Performance Evaluation

### **1. Testing Methodology**
To evaluate the system under realistic, high-stress conditions, a custom, multi-threaded `load_tester.py` script was developed. 
*   **Test Environment:** The test simulated **100 concurrent clients** connecting to the server simultaneously.
*   **Data Volume:** Each of the 100 simulated clients was instructed to sequentially send 10 `UPDATE` commands and 10 `GET` requests (totaling 2,000 intended concurrent requests).
*   **Metrics Measured:** Throughput (requests successfully completed per second), Average Latency (time taken to process a single roundtrip request), and Connection Stability (number of failed/dropped clients).

### **2. Performance Results (Averaged over 3 test runs)**
The load test was executed multiple times to account for warm-up times and ensure consistent evaluation. 

*   **Average Total Processing Time:** `0.48 seconds`
*   **Average Throughput:** `3,436 requests/second`
*   **Average Latency:** `0.53 milliseconds`
*   **Average Connection Failure Rate:** `~28% (28 out of 100 clients failed/dropped)`

### **3. Observations and Analysis**

**A. Exceptional Throughput & Latency (Scalability factor):**
The server's core architecture—specifically the low-level Python `socket` module handling combined with raw `threading`—proved to be incredibly fast. Processing an average of 3,436 requests per second with an individual latency of just 0.53ms per request proves that the fundamental design is highly efficient and capable of handling a very high volume of network traffic without lagging. 

**B. Concurrency Issues (The "Failed Clients" factor):**
Despite the high speed, the server consistently dropped between 25 and 32 connections out of the 100 concurrent clients. 

*   **Root Cause:** This occurs because the server memory—specifically the `leaderboard` dictionary and the `clients` list—is subject to **race conditions**. When 100 threads attempt to write to the dictionary or iterate over the list at the exact same millisecond, Python throws internal runtime errors (e.g., `dictionary changed size during iteration`), which causes the server to severely drop the connection of the affected threads.
*   **Conclusion:** The server handles *sequential* load excellently but fails under aggressive *simultaneous* load due to a lack of thread synchronization.

### **4. Conclusion for Next Steps**
The performance evaluation clearly highlighted the system's speed capabilities while thoroughly diagnosing its primary weakness. The explicit data collected strictly guides our next step in **Optimization and Fixes**: we must introduce `threading.Lock()` to secure shared memory block access, and introduce `try/except` safeguards to ensure connection resilience against unexpected client drops.
