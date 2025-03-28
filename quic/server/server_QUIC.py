import asyncio
import logging
import json
from aioquic.asyncio import serve, QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived
import time

logging.basicConfig(level=logging.INFO) # Logging for debugging

class QuicServerProtocol(QuicConnectionProtocol):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._stream_buffers = {} # Holds incoming data from each incoming stream of data
        self._stream_start_times = {}  # Buffer for start/end time

    def quic_event_received(self, event):

        logging.info("Received QUIC event: %s", event)

        if isinstance(event, StreamDataReceived): # Checks for incoming data

            stream_id = event.stream_id

            if stream_id not in self._stream_start_times: # Starts the stopwatch on the first packet

                self._stream_start_times[stream_id] = time.perf_counter()

            if stream_id not in self._stream_buffers: # Creates a new segment of the buffer to fit the NEW data

                self._stream_buffers[stream_id] = bytearray()

            self._stream_buffers[stream_id].extend(event.data) # Appends the stream of data to an existing one

            if event.end_stream: # All data has been received

                end_time = time.perf_counter() # Ends stopwatch

                # Logs the difference of the start and end of stopwatch
                start_time = self._stream_start_times.pop(stream_id, end_time)
                elapsed_ms = (end_time - start_time) * 1000
                logging.info("File took %.2f ms to receive", stream_id, elapsed_ms)

                data = bytes(self._stream_buffers.pop(stream_id))

                newline_index = data.find(b"\n") # The header contains "\n" from how the client has sent the data

                if newline_index == -1: # Lost the header, something is wrong
                    logging.error("Header not found in stream data")
                    return
                
                header_bytes = data[:newline_index] # Header
                file_data = data[newline_index+1:] # Payload

                try:

                    header = json.loads(header_bytes.decode("utf-8"))
                    filename = header.get("filename", "received_file")
                    expected_size = header.get("filesize", len(file_data))

                    if len(file_data) != expected_size: # Checks that original and the final files are identical in size

                        logging.warning(
                            "Wrong file size: expected %d, got %d",
                            expected_size, len(file_data)
                        )

                    filename = "~" + filename # Adds distinct char to the result filename for differentiation

                    with open(filename, "wb") as f: # Write the file to the same folder as this file (server_QUIC.py)
                        f.write(file_data)

                    logging.info(
                        "Received file '%s' with %d bytes and saved in this file",
                        filename, len(file_data)
                    )

                except Exception as e:

                    logging.error("Error processing stream data: %s", e)

async def main():

    # Loads the TLS certificate and key
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain("ssl_cert.pem", "ssl_key.pem")
    
    logging.info("Starting QUIC server on 127.0.0.1:4433")

    server = await serve("127.0.0.1", 4433, configuration=configuration, create_protocol=QuicServerProtocol)

    try:

        await asyncio.Event().wait() # Runs the server in a loop (forever)

    except KeyboardInterrupt:

        logging.info("Server was closed by YOU, YOURSELF!!!")

    finally:

        server.close()
        await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
