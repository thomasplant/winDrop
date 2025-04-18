import socket
import time
import tkinter as tk
from tkinter import filedialog, scrolledtext

def select_file():
    
    filename = filedialog.askopenfilename() # Opens the file explorer
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def send_file():

    filename = file_entry.get()
    if not filename:
        log_message("Error: No file selected!")
        return
    
    try:
        with open(filename, 'rb') as file:

            while True:
                chunk = file.read(1024)  # Read 1024-byte chunk
                if not chunk:
                    break
                sock.sendall(chunk)  # Send each chunk

            # data = file.read()
            # if not data:
            #     log_message("Error: File is empty!")
            #     return
            
            # # sock.send(data.encode())
            # sock.sendall(data)
            sock.sendall(b"EOF")  # Send EOF marker (MUST HAVE)
            log_message(f"Sent file: {filename}")

    except IOError as error:
        log_message(f"Error: {error}")

def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, "------------------------------------------------------------" + "\n")
    log_text.see(tk.END)

host = '10.10.10.5'
# host = '192.168.182.170' # Use the actual server IP address
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4, TCP)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (IPv4, UDP)
for _ in range(20):
    try:
        sock.connect((host, port))
        break
    except ConnectionRefusedError:
        time.sleep(2)

root = tk.Tk()
root.title("Sender")

tk.Label(root, text="Select a file to send:").pack()

file_entry = tk.Entry(root, width=50)
file_entry.pack()

tk.Button(root, text="Browse", command=select_file).pack()
tk.Button(root, text="Send File", command=send_file).pack()

log_text = scrolledtext.ScrolledText(root, width=60, height=10)
log_text.pack()

root.mainloop()

sock.close()