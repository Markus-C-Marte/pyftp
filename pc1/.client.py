import socket

def start_client():
    # Define the path for the Unix socket file
    socket_path = "./socket"

    # Create a Unix domain socket
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    print(f"Connecting to server at {socket_path}")
    client_socket.connect(socket_path)

    try:
        # Send a message to the server
        message = "Hello, Server!"
        print(f"Sending: {message}")
        client_socket.sendall(message.encode())

        # Receive the server's response
        response = client_socket.recv(1024)
        print(f"Received: {response.decode()}")
    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    start_client()

