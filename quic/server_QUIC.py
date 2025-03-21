import asyncio
import ssl
import tkinter as tk
from tkinter import scrolledtext
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import StreamDataReceived
import time

class FileReceiverProtocol(QuicConnectionProtocol):
    def __init__(self, *args, log_callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._stream_data = {}
        self.log_callback = log_callback

    def quic_event_received(self, event):
        log_message("Receiving files!")
        if isinstance(event, StreamDataReceived):
            stream_id = event.stream_id
            data = event.data

            if stream_id not in self._stream_data:
                self._stream_data[stream_id] = {
                    'chunks': [],
                    'start': time.perf_counter()
                }

            self._stream_data[stream_id]['chunks'].append(data)

            if event.end_stream:
                total_data = b"".join(self._stream_data[stream_id]['chunks'])
                total_data = total_data.replace(b"EOF", b"")
                filename = f"output_quic_{stream_id}.bin"

                with open(filename, "wb") as f:
                    f.write(total_data)

                end_time = time.perf_counter()
                duration_ms = (end_time - self._stream_data[stream_id]['start']) * 1000
                if self.log_callback:
                    self.log_callback(f"Received file {filename}")
                    self.log_callback(f"Transfer time: {duration_ms:.2f} ms")

async def run_server(log_callback):
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain("server-cert.pem", "server-key.pem")
    await serve("0.0.0.0", 4433, configuration=configuration,
                create_protocol=lambda *args, **kwargs: FileReceiverProtocol(*args, log_callback=log_callback, **kwargs))

def start_server():
    log_message("Starting QUIC server on port 4433...")
    asyncio.get_event_loop().create_task(run_server(log_message))

def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.insert(tk.END, "------------------------------------------------------------\n")
    log_text.see(tk.END)

root = tk.Tk()
root.title("QUIC Server - File Transfer")
tk.Button(root, text="Start QUIC Server", command=start_server).pack()
log_text = scrolledtext.ScrolledText(root, width=60, height=10)
log_text.pack()
asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))  # Give control to UI
root.mainloop()