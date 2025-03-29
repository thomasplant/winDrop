import socket
import struct
import os

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080        # The port used by the server

# Prompt for user to choose which file with path
filepath = input("Enter the path to the file to send: ").strip()
if not os.path.isfile(filepath):

    print("File does not exist!")
    exit(1)

# Get file details
filename = os.path.basename(filepath)
filename_bytes = filename.encode('utf-8')
file_size = os.path.getsize(filepath)

# Building the metadata (header) of the file being sent
filename_length_str = str(len(filename_bytes)).zfill(4) # Filename length (4 char long)
file_size_str = str(file_size).zfill(8) # File Size (8 char long)
header = filename_length_str.encode('utf-8') + filename_bytes + file_size_str.encode('utf-8') 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    client_socket.connect((HOST, PORT))

    print(f"Connected to server at {HOST}:{PORT}")
    
    # Send the header first
    client_socket.sendall(header)
    
    # Now send the file content in chunks
    with open(filepath, "rb") as f:

        while True:

            chunk = f.read(4096)

            if not chunk:

                break

            client_socket.sendall(chunk)

    print("File sent successfully!")
