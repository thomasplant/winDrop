import socket
from time import sleep
import tkinter as tk
from tkinter import filedialog, scrolledtext
from datetime import datetime, timedelta



def select_file():
    
    filename = filedialog.askopenfilename() # Opens the file explorer
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def send_file():

    filename = file_entry.get()
    read_file_size = read_size_entry.get()
    
    if not read_file_size:
        read_file_size = 1024
    else:
        read_file_size = int(read_file_size)

    if not filename:
        log_message("Error: No file selected!")
        return
    
    try:
        with open(filename, 'br') as file:
            
            data = file.read(read_file_size)
            while len(data) > 0:
                sock.sendto(data, (host, port))
                sleep(0.0002)
                log_message(f'packet sent!')
                data = file.read(read_file_size)
            
            sock.sendto(b'<EOF/>', (host, port))
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
host = '192.168.182.160'
#host = 'localhost' # Use the actual server IP address
port = 8080
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4, TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (IPv4, UDP)
#sock.connect((host, port))
sock.setblocking(False)

root = tk.Tk()
root.title("Sender")

tk.Label(root, text="Select a file to send:").pack()

file_entry = tk.Entry(root, width=50)
file_entry.pack()

tk.Button(root, text="Browse", command=select_file).pack()
tk.Button(root, text="Send File", command=send_file).pack()

read_size_entry = tk.Entry(root, width=10)
read_size_entry.pack()

tk.Label(root, text="Select how big of packets to send").pack()
log_text = scrolledtext.ScrolledText(root, width=60, height=10)
log_text.pack()

root.mainloop()
