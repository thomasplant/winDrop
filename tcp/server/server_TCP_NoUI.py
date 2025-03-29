import socket
import struct
import time
import datetime

HOST = '127.0.0.1'  # Localhost
PORT = 8080        # Non-privileged port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}...")
    
    conn, addr = server_socket.accept()

    with conn:

        print("Connected by", addr)

        start_time = time.perf_counter()  # Start timing
        
        # First, receive 4 bytes representing the length of the filename
        raw_filename_len = conn.recv(4)
        if len(raw_filename_len) < 4:
            print("Failed to receive the filename length.")
            exit(1)
        filename_len = struct.unpack("!I", raw_filename_len)[0]
        
        # Receive the filename using the length obtained
        filename_bytes = conn.recv(filename_len)
        filename = filename_bytes.decode('utf-8')
        
        # Next, receive 8 bytes representing the file size
        raw_filesize = conn.recv(8)
        if len(raw_filesize) < 8:
            print("Failed to receive the file size.")
            exit(1)
        file_size = struct.unpack("!Q", raw_filesize)[0]
        print(f"Receiving file: {filename} of size: {file_size} bytes")
        
        filename = "~" + filename # Adds distinct char to the result filename for differentiation

        with open(filename, "wb") as f: # Write the file to the same folder as this file (server_QUIC.py)

            bytes_received = 0

            while bytes_received < file_size:

                chunk = conn.recv(4096) # Receive in chunks (here 4096 bytes per chunk)

                if not chunk:

                    break

                f.write(chunk)

                bytes_received += len(chunk)

        end_time = time.perf_counter()  # End timing
        transfer_time = (end_time - start_time) * 1000 # Convert to ms
        
        print(f"File transfer took {transfer_time:.6f} ms")
        print(f"Received file successfully! New filename: {filename}")
