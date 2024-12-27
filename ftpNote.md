
# Socket Study: File transfer client

## Reference
*A File Transfer Client :: Unix Socket :: Python*
___


```python 
import socket

def start_client():
    socket_path = "../socket"
    cargo_file_path ="io/INFILE"
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
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
```
### Breakdown
___
>[!warning] Dependencies
___
The file above depends on an an already existing
==Unix Socket== **and** A ***small file to be transfered*** 
___
>[!Summary]
>___
The File above is an example of a *Socket Client* 
as opposed to a *Socket Server*.
This client, when provided with a 
== target socket == and a  == payload file == 
will connect to the socket, and deliver the payload
in a series of chunks as to not overwhelm buffers,
the server or the network.
___
> [!Example] PROCEDURE
>___
1. Establish The Connection
== >PATH TO SOCKET< ==
    1. ::   prep the socket to server type
    2. ::   connect the socket using == Path provided ==

2. After Connected:: Deliver Payload
== >REQS PAYLOAD< == == >REQS CONNECTION< ==
    1. :: Socket Send `Payload file name".encode()`
    2. :: Read chunk of payload, send chunks as bytes
    3. :: When Done ***Recieve Responce*** 

>[!CAUTION] FTP is build around Responding and Recieving 
    >This is to make sure connections arent lost
    >or processes dropped

3. Clean-Up: Close socket and File
___

# Socket Study: Socket Server

## Example
*File Transfer Server:: Recieve and Write File:: Unix Socket*
___
[!CAUTION] this ones a bit bigger so we'll take it in steps

1. **!SANITY CHECK!** *Assure Socket Doen't Exist*
___
```python
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
```

2. **Prep Socket, Bind to Location, Listen for Clients**
___
```python
    # Create a Unix domain socket
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the file
    server_socket.bind(socket_path)
    print(f"Server started at {socket_path}")

    # Listen for incoming connections
    server_socket.listen(1)
    print("Waiting for a connection...")

    
```


3. **ON CONNECTION RECIEVE, RECORD THEN RESPOND**
___
```python
# Accept a connection
    conn, addr = server_socket.accept()
    print("Connection established!")

    try:
        ofile = b"" # <-- See Below
        while True:
            # Receive data
            data = conn.recv(1024)
            if not data:
                break
            ofile+=data               #<-- 
            print(f"Received: {data.decode()}")

            # Send a response
            conn.sendall(b"Message received!")

```
___
>[!TIP] :: Closer Look :: Stuffs A Little Odd :: 
>___
>**ofile = b""**    
::  setting b before a String makes it *Binary*  (TCP Convention?)
::  We will add each chunk we get to this string to record the message
>**data = conn.recv(1024)**
::  conn is the accepted socket connection
::  we are recieving 1024 bytes (bits?) per chunk
::  we're using ==data== to write the chunks to ofile
::  as well as printing the decoded chunk on arrival
>**try: while True: if not data: break**
::  When theres no more message == if not data: break == 
::      will bring us to == finally == block.
::  Since we donk know how big the transfer is
::      while true will keep us going
>**ofile+=data**
::  EVERY read chunk gets appended to ofile.
::  After reading is done we will use ofile to reconstruct
:;  the file the connection was referencing 
>**conn.sendall(b`"Message recieved!"`)**
::  After EVERY message we send a responce it's expected
:: and confirms nothing is dropped
___




4. RECONSTRUCTING FROM JUST BITS 
___
```python
finally:
        # Close the connection and clean up
        file_name, file_content = ofile.decode().split('\n', 1)

        # Write the file contents to a new file
        with open(file_name, 'w') as f:
            f.write(file_content)

        print(f"{ofile.decode()}")
```
___
>[!CAUTION] WHY WE SEND FILENAME FIRST
>___
>before the client even opens the file the following code is executed
::     `client_socket.sendall(f"INFILE\n".encode())`
that is the *FILENAME* a *NEW LINE SYMBOL* AND encoded into bits
this makes it so the filename is bundled ==WITH== the data and anything
sent this way can be easily handled by splitting via *\n once* ==('\n', 1)==
this convention will help if we want to do a bunch of files
if we want to know the name but not decode the data we can still
store the data as file_content.encode(), this shit rules.
___




5. cleanup
___
```python
        conn.close()
        server_socket.close()
        os.unlink(socket_path)

if __name__ == "__main__":
    start_server()
```
