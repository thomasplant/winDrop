import asyncio
import threading
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
        self.log_callback = log_callback
        self.file_buffer = {}
        self.start_time = {}
        print("connected")

    def quic_event_received(self, event):
        print("entered quic event received")
        if isinstance(event, StreamDataReceived):
            print("Data receiving")
            sid = event.stream_id
            if sid not in self.file_buffer:
                self.file_buffer[sid] = []
                self.start_time[sid] = time.perf_counter()
                if self.log_callback:
                    self.log_callback("Receiving new stream...")

            self.file_buffer[sid].append(event.data)

            if event.end_stream:
                content = b"".join(self.file_buffer[sid]).replace(b"EOF", b"")
                filename = f"output_quic_{sid}.bin"
                with open(filename, "wb") as f:
                    f.write(content)
                duration = (time.perf_counter() - self.start_time[sid]) * 1000
                if self.log_callback:
                    self.log_callback(f"Received file: {filename}")
                    self.log_callback(f"Transfer time: {duration:.2f} ms")

                # ✅ Send ACK back to client
                self._quic.send_stream_data(stream_id, b"ACK", end_stream=True)

async def run_server_async(log_callback):
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain("server-cert.pem", "server-key.pem")

    print("Waiting for soemone to connect")
    await serve(
        "0.0.0.0", 4433,
        configuration=config,
        create_protocol=lambda *args, **kwargs: FileReceiverProtocol(*args, log_callback=log_callback, **kwargs)
    )

    while True:
        await asyncio.sleep(3600)

def start_server():
    log_message("Starting QUIC server on port 4433...")

    def runner():
        asyncio.run(run_server_async(log_message))

    threading.Thread(target=runner, daemon=True).start()

def log_message(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.insert(tk.END, "-"*60 + "\n")
    log_text.see(tk.END)

# GUI
root = tk.Tk()
root.title("QUIC Receiver")

tk.Button(root, text="Start QUIC Server", command=start_server).pack()
log_text = scrolledtext.ScrolledText(root, width=60, height=15)
log_text.pack()

root.mainloop()
