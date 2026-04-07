# Secure Multi-Threaded Leaderboard System

A high-performance, secure, and concurrent leaderboard system implemented using low-level Python socket programming and TLS/SSL encryption.

## 🚀 Project Overview
This project demonstrates a robust Client-Server architecture designed to handle multiple concurrent users securely. It allows clients to update their scores and retrieve a real-time leaderboard, with all communications encrypted via SSL/TLS.

### Key Features
- **Low-Level Socket Programming:** Built using the `socket` module without high-level frameworks.
- **TLS/SSL Encryption:** Secure communication using self-signed certificates and the `ssl` module.
- **Multi-Threading:** Handles numerous concurrent client connections simultaneously using `threading`.
- **Thread Safety:** Implements `threading.Lock` to ensure data integrity under high concurrency.
- **Performance Optimized:** Capable of handling over 6,000 requests per second.

---

## 🏗 Architecture
The system follows a **Client-Server** model:
1.  **Server:** A multi-threaded engine that listens for secure connections, manages a dictionary of scores, and broadcasts updates to all connected clients.
2.  **Client:** A secure terminal interface that allows users to send `UPDATE` and `GET` commands.
3.  **Security Layer:** An SSL wrapper that upgrades standard TCP sockets to encrypted TLS tunnels.

---

## 🛠 Setup & Installation

### Prerequisites
- Python 3.x
- `cryptography` library (for certificate generation)

### Installation
```bash
# Install required dependencies
python3 -m pip install cryptography --break-system-packages
```

### 1. Generate Security Certificates
Run the generation script to create `cert.pem` and `key.pem`:
```bash
python3 generate_cert.py
```

### 2. Start the Server
```bash
python3 server.py
```
*Note: The server is configured to listen on all interfaces (`0.0.0.0`) on port `5555`.*

### 3. Start the Client
```bash
python3 client.py
```

---

## 🎮 Usage Instructions
Once the client is connected, use the following commands:
- `UPDATE <name> <score>`: Upload a new score for a user (e.g., `UPDATE Alice 100`).
- `GET`: Retrieve the current top scores.
- `EXIT`: Safely close the connection.

---

## 📊 Performance & Optimization
The system was rigorously tested using a custom load balancer simulating 100 concurrent clients.

| Metric | Result |
| :--- | :--- |
| **Max Throughput** | ~6,500 requests/second |
| **Avg Latency** | 0.73 ms |
| **Failure Rate** | 0% (Post-Optimization) |

### Optimization Highlights
- **Concurrency Fix:** Added `threading.Lock` to resolve race conditions.
- **Throughput Boost:** Increased socket backlog to 100 to handle connection bursts.
- **Resilience:** Implemented robust error handling for abrupt disconnections and invalid protocol inputs.

---

## 📄 License
This project was developed for the Computer Networks (CN) Course - Semester 4.
