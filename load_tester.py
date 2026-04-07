import socket
import ssl
import threading
import time

HOST = '127.0.0.1' # localhost - server running on this machine
PORT = 5555
NUM_CLIENTS = 100       # Number of concurrent clients to simulate
REQUESTS_PER_CLIENT = 10 # Requests each client makes

success_count = 0
failure_count = 0
total_latency = 0
lock = threading.Lock()

def simulate_client(client_id):
    global success_count, failure_count, total_latency
    
    # Create SSL context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        # Establish connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(sock, server_hostname=HOST)
        secure_sock.connect((HOST, PORT))

        for i in range(REQUESTS_PER_CLIENT):
            start_time = time.time()
            
            # Send an update command
            msg = f"UPDATE Bot_{client_id} {i*10}"
            secure_sock.send(msg.encode())
            
            # Receive broadcast
            secure_sock.recv(4096)
            
            # Send a get command
            secure_sock.send(b"GET")
            secure_sock.recv(4096)
            
            end_time = time.time()
            latency = end_time - start_time
            
            with lock:
                success_count += 2 # 2 requests sent (UPDATE and GET)
                total_latency += latency
                
        # Graceful disconnect
        secure_sock.send(b"EXIT")
        secure_sock.close()

    except Exception as e:
        # Catch unexpected drops (server crash or timeouts)
        with lock:
            failure_count += 1
            # print(f"Client {client_id} failed: {e}")

def run_load_test():
    print(f"Starting load test with {NUM_CLIENTS} concurrent clients.")
    print(f"Each client will send {REQUESTS_PER_CLIENT} UPDATEs and {REQUESTS_PER_CLIENT} GETs.")
    print("...")
    
    start_time = time.time()
    
    threads = []
    
    # Spawn multiple threads (clients) simultaneously
    for i in range(NUM_CLIENTS):
        thread = threading.Thread(target=simulate_client, args=(i,))
        threads.append(thread)
        thread.start()
        
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
        
    end_time = time.time()
    
    total_time = end_time - start_time
    total_requests = success_count
    
    print("\n=== Performance Results ===")
    print(f"Total Time Taken:     {total_time:.2f} seconds")
    print(f"Total Requests Sent:  {total_requests}")
    print(f"Successful Requests:  {success_count}")
    print(f"Failed Clients:       {failure_count}")
    
    if success_count > 0:
        throughput = total_requests / total_time
        avg_latency = (total_latency / (success_count / 2)) * 1000 # Convert to ms
        print(f"Throughput:           {throughput:.2f} requests/second")
        print(f"Average Latency:      {avg_latency:.2f} ms")


if __name__ == "__main__":
    run_load_test()
