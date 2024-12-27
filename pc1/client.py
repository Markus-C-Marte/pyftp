import socket

def start_client():
    # Define the path for the Unix socket file
    socket_path = "../socket"
    cargo_file_path ="io/INFILE"

    # Create a Unix domain socket
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    print(f"Connecting to server at {socket_path}")
    client_socket.connect(socket_path)

    try:
        client_socket.sendall(f"INFILE\n".encode())
        with open( cargo_file_path , "rb") as f:
            while chunk:= f.read(1024):
                client_socket.sendall(chunk)

        # Receive the server's response
        response = client_socket.recv(1024)
        print(f"Received: {response.decode()}")
    finally:
        # Close the socket
        client_socket.close()
            

if __name__ == "__main__":
    start_client()

