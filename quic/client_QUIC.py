import asyncio
import tkinter as tk
from tkinter import filedialog, scrolledtext
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration

server_ip = "127.0.0.1"
port = 4433

def select_file():
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def send_file_wrapper():
    filename = file_entry.get()
    if not filename:
        log_message("Error: No file selected!")
        return
    asyncio.run(send_file(filename))

async def send_file(filename):
    try:
        configuration = QuicConfiguration(is_client=True)
        async with connect(server_ip, port, configuration=configuration) as connection:
            stream_id = connection._quic.get_next_available_stream_id()
            with open(filename, 'rb') as f:
                chunk = f.read(1024)
                while chunk:
                    await connection.send_stream_data(stream_id, chunk, end_stream=False)
                    chunk = f.read(1024)
                await connection.send_stream_data(stream_id, b"EOF", end_stream=True)
            log_message(f"Sent file: {filename}")
    except Exception as e:
        log_message(f"Error sending file: {e}")

def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, "------------------------------------------------------------\n")
    log_text.see(tk.END)

root = tk.Tk()
root.title("QUIC Client - File Sender")

tk.Label(root, text="Select a file to send:").pack()
file_entry = tk.Entry(root, width=50)
file_entry.pack()
tk.Button(root, text="Browse", command=select_file).pack()
tk.Button(root, text="Send File", command=send_file_wrapper).pack()

log_text = scrolledtext.ScrolledText(root, width=60, height=10)
log_text.pack()
root.mainloop()