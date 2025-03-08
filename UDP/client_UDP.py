import socket
import tkinter as tk
from tkinter import filedialog, scrolledtext
from datetime import datetime, timedelta

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
        with open(filename, 'r') as file:
            
            data = file.read(1024)
            while len(data) > 0:

                sock.sendto(data.encode(), (host, port))
                data = file.read(1024)
            log_message(f"Sent file: {filename}")

    except IOError as error:
        log_message(f"Error: {error}")

def log_message(message):
    now = datetime.now()

    log_text.insert(tk.END, f"--------- Time: {(now - START_TIME ).total_seconds()* 1000} -------------------- \n")
    log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, "------------------------------------------------------------" + "\n")
    log_text.see(tk.END)



START_TIME = datetime.now()
# host = '127.0.0.1'
host = 'localhost' # Use the actual server IP address
port = 8080
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4, TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (IPv4, UDP)
#sock.connect((host, port))

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
