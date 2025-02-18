import socket
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
        with open(filename, 'r') as file:
            data = file.read()
            if not data:
                log_message("Error: File is empty!")
                return
            
            sock.send(data.encode())
            log_message(f"Sent file: {filename}")

    except IOError as error:
        log_message(f"Error: {error}")

def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, "------------------------------------------------------------" + "\n")
    log_text.see(tk.END)

host = '127.0.0.1'
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4, TCP)
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (IPv4, UDP)
sock.connect((host, port))

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