from datetime import datetime
import socket
import threading # Solves issue with waiting for sender/clients
import tkinter as tk
from tkinter import scrolledtext

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

        start_time = datetime.now()
        clients = set() 
        sock.setblocking(False)
        fileno = 0

        while len(clients) < total_clients:

        # Receiving files
            try:
                data, address = sock.recvfrom(1024)
                if address not in clients:
                    clients.add(address)
                    log_message(f"Starting  to recieve data from client {len(clients)}: {address}", start_time)

                    
                    filename = f'output{fileno}.txt'
                    fileno = fileno + 1

                    with open(filename, 'w') as fileopen:
                        while data:
                            fileopen.write(data.decode())
                            try:
                                data, _ = sock.recvfrom(1024)
                            except BlockingIOError:
                                break

                    
                    log_message(f"Received file successfully! New filename: {filename}", start_time)
            except:
                #No data case
                pass
        

        log_message(f"all files have been sent from max amount of clients. Shutting down server", start_time)


    except Exception as e:
        log_message(f"Error: {e}")

def log_message(message, start_time=datetime.now()):
    root.after(0, lambda: _log_message(message, start_time))

def _log_message(message, start_time):
    time = datetime.now()

    log_text.insert(tk.END, f"--------- Time in MS: {(time - start_time).total_seconds()* 1000} --------------------- \n")
    log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, "------------------------------------------------------------" + "\n")
    log_text.see(tk.END)

host = "localhost" # This allows connections from any machine on the network
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (IPv4, UDP)
sock.bind((host, port))

root = tk.Tk()
root.title("UDP Receiver")

tk.Label(root, text="How many clients are you connecting with?").pack()

client_entry = tk.Entry(root, width=10)
client_entry.pack()

tk.Button(root, text="Start Server", command=start_server).pack()

log_text = scrolledtext.ScrolledText(root, width=60, height=10)
log_text.pack()

root.mainloop()