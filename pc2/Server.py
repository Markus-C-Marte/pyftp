import socket
import os

def start_server():
    # Define the path for the Unix socket file
    socket_path = "../socket"

    # Ensure the socket does not already exist
    try:
        os.unlink(socket_path)
    except FileNotFoundError:
        pass

    # Create a Unix domain socket
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the file
    server_socket.bind(socket_path)
    print(f"Server started at {socket_path}")

    # Listen for incoming connections
    server_socket.listen(1)
    print("Waiting for a connection...")

    # Accept a connection
    conn, addr = server_socket.accept()
    print("Connection established!")

    try:
        ofile = b""
        while True:
            # Receive data
            data = conn.recv(1024)
            if not data:
                break
            ofile+=data
            print(f"Received: {data.decode()}")

            # Send a response
            conn.sendall(b"Message received!")
    finally:
        # Close the connection and clean up
        file_name, file_content = ofile.decode().split('\n', 1)

        # Write the file contents to a new file
        with open(file_name, 'w') as f:
            f.write(file_content)

        print(f"{ofile.decode()}")
        conn.close()
        server_socket.close()
        os.unlink(socket_path)

if __name__ == "__main__":
    start_server()

