import socket
import ssl
import threading

HOST = '0.0.0.0'
PORT = 5555

leaderboard = {}
clients = []
data_lock = threading.Lock() # Lock for thread-safe access to shared data

def broadcast(message):
    encoded_msg = message.encode()
    with data_lock:
        # Create a copy to iterate safely
        for c in list(clients):
            try:
                c.send(encoded_msg)
            except:
                try:
                    clients.remove(c)
                except:
                    pass

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")
    with data_lock:
        clients.append(conn)

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            parts = data.split()
            if not parts:
                continue

            command = parts[0].upper()

            if command == "UPDATE":
                if len(parts) < 3:
                    conn.send("[ERROR] Usage: UPDATE <name> <score>\n".encode())
                    continue
                
                name = parts[1]
                try:
                    score = int(parts[2])
                    with data_lock:
                        leaderboard[name] = score
                        print(f"[UPDATE] {name} -> {score}")
                        # Prepare message while under lock to ensure consistency
                        sorted_board = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
                        msg = "\n".join([f"{i+1}. {n} - {s}" for i,(n,s) in enumerate(sorted_board)])
                    
                    broadcast("\n=== Leaderboard ===\n" + msg)
                except ValueError:
                    conn.send("[ERROR] Score must be an integer\n".encode())

            elif command == "GET":
                with data_lock:
                    sorted_board = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
                    msg = "\n".join([f"{i+1}. {n} - {s}" for i,(n,s) in enumerate(sorted_board)])
                conn.send(("\n=== Leaderboard ===\n" + msg + "\n").encode())

            elif command == "EXIT":
                break
            
            else:
                conn.send("[ERROR] Unknown command\n".encode())

    except (ConnectionResetError, BrokenPipeError):
        print(f"[FORCE DISCONNECT] {addr}")
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        with data_lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"[DISCONNECTED] {addr}")

def start():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(100)

    print(f"[STARTED] Server running on {HOST}:{PORT}")

    secure_server = context.wrap_socket(server, server_side=True)

    while True:
        try:
            conn, addr = secure_server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except ssl.SSLError as e:
            print(f"[SSL ERROR] Handshake failed: {e}")
        except Exception as e:
            print(f"[SERVER ERROR] {e}")

start()