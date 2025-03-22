import asyncio
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
import ssl

server_ip = "127.0.0.1"  # Replace with server IP if needed
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

    def runner():
        try:
            asyncio.run(send_file(filename))
        except Exception as e:
            import traceback
            log_message(f"Error: {type(e).__name__} - {e}")
            traceback.print_exc()

    threading.Thread(target=runner, daemon=True).start()

async def send_file(filename):
    config = QuicConfiguration(is_client=True)
    config.verify_mode = ssl.CERT_NONE  # For testing only

    log_message("Connecting to server...")
    print("Client is still connecting to server")

    async with connect(server_ip, port, configuration=config) as connection:
        print("Client side connected")
        log_message("Connected! Sending file...")

        sid = connection._quic.get_next_available_stream_id()
        with open(filename, 'rb') as f:
            chunk = f.read(1024)
            while chunk:
                await connection.send_stream_data(sid, chunk, end_stream=False)
                chunk = f.read(1024)
            await connection.send_stream_data(sid, b"EOF", end_stream=True)

        log_message(f"File sent: {filename}")

def log_message(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.insert(tk.END, "-"*60 + "\n")
    log_text.see(tk.END)

# GUI
root = tk.Tk()
root.title("QUIC Sender")

tk.Label(root, text="Select a file to send:").pack()
file_entry = tk.Entry(root, width=50)
file_entry.pack()
tk.Button(root, text="Browse", command=select_file).pack()
tk.Button(root, text="Send File", command=send_file_wrapper).pack()
log_text = scrolledtext.ScrolledText(root, width=60, height=15)
log_text.pack()

root.mainloop()
