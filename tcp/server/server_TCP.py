import socket
import threading # Solves issue with waiting for sender/clients
import tkinter as tk
from tkinter import scrolledtext
import time
import datetime

def start_server():
    """ Starts the server in a separate thread """
    try:
        total_clients = int(client_entry.get())
        log_message(f"Server started, waiting for {total_clients} clients...")

        threading.Thread(target=server_logic, args=(total_clients,), daemon=True).start()
    
    except ValueError:
        log_message("Error: Please enter a valid number of clients!")

def server_logic(total_clients):

    try:
        sock.listen(total_clients)
        connections = []

        for i in range(total_clients):
            conn, addr = sock.accept()
            connections.append(conn) # Stores into connections list
            log_message(f"Connected with client {i + 1}")

        # Receiving files
        fileno = 0
        for conn in connections:
            data = conn.recv(1024)
            if not data:
                continue
            
            fileno = fileno + 1
            filename = f'output{fileno}'

            start_time = time.perf_counter()  # Start timing

            with open(filename, 'wb') as fileopen:
                # start_time = time.perf_counter()  # Start timing
                fileopen.write(data)
                while True: 
                    data = conn.recv(1024)
                    if not data or data.endswith(b"EOF"):  # Detect end of file
                        break
                    fileopen.write(data)
                # end_time = time.perf_counter()  # End timing

            end_time = time.perf_counter()  # End timing
            transfer_time = (end_time - start_time) * 1000 # Convert to ms
            
            log_message(f"Received file successfully! New filename: {filename}")
            log_message(f"File transfer took {transfer_time:.6f} ms")

        for conn in connections: # Closing all connections
            conn.close()
        log_message("Server shut down")

    except Exception as e:
        log_message(f"Error: {e}")

def log_message(message):
    """ Logs messages to the UI in a thread-safe way """
    log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, "------------------------------------------------------------" + "\n")
    log_text.see(tk.END)

# host = "127.0.0.1" # Replace with server's local IP address
host = "0.0.0.0" # This allows connections from any machine on the network
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4, TCP)
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (IPv4, UDP)
sock.bind((host, port))

root = tk.Tk()
root.title("Receiver")

tk.Label(root, text="How many clients are you connecting with?").pack()

client_entry = tk.Entry(root, width=10)
client_entry.pack()

tk.Button(root, text="Start Server", command=start_server).pack()

log_text = scrolledtext.ScrolledText(root, width=60, height=10)
log_text.pack()

root.mainloop()