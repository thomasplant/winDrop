"""
Make sure to run this command line first:  
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server-key.pem -out server-cert.pem
"""

import asyncio
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived
import tkinter as tk
from tkinter import scrolledtext

class FileTransferServer(QuicConnectionProtocol):
    """ QUIC Server to receive file data """

    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            filename = f"output_quic.txt"
            with open(filename, "wb") as file:
                file.write(event.data)
            log_message(f"Received file successfully! Saved as {filename}")

def log_message(message):
    """ Logs messages to the UI """
    log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, "-" * 60 + "\n")
    log_text.see(tk.END)

async def run_server():
    """ Starts QUIC server """
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain("server-cert.pem", "server-key.pem")  # Required for QUIC
    await serve("0.0.0.0", 8080, configuration=configuration, create_protocol=FileTransferServer)
    # Try port 4433 if 8080 doesn't work

def start_server():
    asyncio.run(run_server())

root = tk.Tk()
root.title("QUIC Server - File Transfer")

tk.Button(root, text="Start QUIC Server", command=start_server).pack()
log_text = scrolledtext.ScrolledText(root, width=60, height=10)
log_text.pack()

root.mainloop()
