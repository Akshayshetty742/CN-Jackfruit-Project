import socket
import ssl

HOST = '10.30.201.41'
PORT = 5555

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_sock = context.wrap_socket(sock, server_hostname=HOST)
secure_sock.connect((HOST, PORT))

print("Connected to server")

while True:
    msg = input("Enter command (UPDATE name score / GET / EXIT): ")

    if msg == "EXIT":
        break

    try:
        secure_sock.send(msg.encode())
        data = secure_sock.recv(4096).decode()
        if not data:
            print("Server closed connection.")
            break
        print(data)
    except (ConnectionResetError, BrokenPipeError):
        print("Lost connection to server.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break

secure_sock.close()
