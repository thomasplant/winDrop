import socket
import threading # Solves issue with waiting for sender/clients
import tkinter as tk
from tkinter import W, scrolledtext
import time

def start_server():
    """ Starts the server in a separate thread """
    try:
        total_clients = int(client_entry.get())
        recieve_file_size = int(recieve_size_entry.get())

        log_message(f"Server started, waiting for {total_clients} clients...")

        threading.Thread(target=server_logic, args=(total_clients, recieve_file_size), daemon=True).start()
    
    except ValueError:
        log_message(f"Server started, waiting for {1} clients...")

        threading.Thread(target=server_logic, args=(1,1024,), daemon=True).start()

def server_logic(total_clients, recieve_file_size):

    try:

        clients = set() 
        sock.setblocking(False)
        fileno = 0

        while len(clients) < total_clients:

        # Receiving files
            try:
                data, address = sock.recvfrom(recieve_file_size)
                if address not in clients:
                    clients.add(address)
                    start_time = time.perf_counter() 
                    log_message(f"Starting  to recieve data from client {len(clients)}: {address}", start_time)

                    
                    filename = f'output{fileno}.txt'
                    fileno = fileno + 1

                    with open(filename, 'bw') as fileopen:
                        #First recieve
                        if((b'<EOF/>' in data)):
                            data = data.replace(b'<EOF/>', b'')
                            fileopen.write(data)
                            log_message(f"Received file successfully! New filename: {filename}", start_time)
                        else:
                            fileopen.write(data)

                        #After First recieve
                        while True:
                            if((b'<EOF/>' in data)):
                                data = data.replace(b'<EOF/>', b'')
                                fileopen.write(data)
                                end_time = time.perf_counter()
                                log_message(f"Received file successfully! New filename: {filename}", start_time, end_time)
                                break;

                            else:
                                try:
                                    data, _ = sock.recvfrom(recieve_file_size)
                                    fileopen.write(data)
                                    #got here
                                except BlockingIOError:
                                    pass

                        filename.close()

            except:
                #No data case
                pass
        



    except Exception as e:
        log_message(f"Error: {e}")

def log_message(message, start_time=time.perf_counter(), end_time=None):
    root.after(0, lambda: _log_message(message, start_time, end_time))

def _log_message(message, start_time, end_time):

    if(end_time != None ):
        log_text.insert(tk.END, f"--------- Time in MS: {(end_time - start_time)* 1000} --------------------- \n")
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

tk.Label(root, text="Select how big of packets to recieve").pack()
recieve_size_entry = tk.Entry(root, width=10)
recieve_size_entry.pack()

tk.Button(root, text="Start Server", command=start_server).pack()

log_text = scrolledtext.ScrolledText(root, width=60, height=10)
log_text.pack()

root.mainloop()