import asyncio
from aioquic.asyncio.client import connect
from aioquic.quic.configuration import QuicConfiguration
import tkinter as tk
from tkinter import filedialog, scrolledtext

async def send_file():
    filename = file_entry.get()
    if not filename:
        log_message("Error: No file selected!")
        return

    configuration = QuicConfiguration(is_client=True)
    
    async with connect(server_ip, 4433, configuration=configuration) as protocol:
        with open(filename, "rb") as file:
            data = file.read()
            protocol._quic.send_stream_data(0, data)
            log_message(f"Sent file: {filename}")

def select_file():
    """ Opens a file dialog for the user to select a file to send """
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def log_message(message):
    """ Logs messages to the UI """
    log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, "-" * 60 + "\n")
    log_text.see(tk.END)

# Replace with actual server IP address
# server_ip = "192.168.X.X"  # Change to the real QUIC server IP
server_ip = "127.0.0.1"  # Localhost for same-machine testing


# Tkinter UI
root = tk.Tk()
root.title("QUIC Client - File Transfer")

tk.Label(root, text="Select a file to send:").pack()
file_entry = tk.Entry(root, width=50)
file_entry.pack()
tk.Button(root, text="Browse", command=select_file).pack()
# tk.Button(root, text="Send File", command=lambda: asyncio.run(send_file())).pack()
tk.Button(root, text="Send File", command=lambda: asyncio.create_task(send_file())).pack()


log_text = scrolledtext.ScrolledText(root, width=60, height=10)
log_text.pack()

root.mainloop()
