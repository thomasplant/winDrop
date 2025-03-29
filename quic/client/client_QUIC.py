import asyncio
import logging
import ssl
import json
import os
import time
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration

logging.basicConfig(level=logging.INFO) # Logging for debugging

async def main():

    # Certificate verification
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = ssl.CERT_NONE

    # Prompt for user to choose which file with path
    #
    # file_path = input("Enter the path to the file to send (Needs to be the full path): ")
    file_path = "./5MB.txt"
    try:

        with open(file_path, "rb") as f:
            file_content = f.read()

    except Exception as e:

        logging.error("There is an error with reading files: %s", e)
        return

    # Gets the file name from the path
    filename = os.path.basename(file_path)

    # Need to send file information for server to confirm if everything is correct and what the filename is
    header = json.dumps({
        "filename": filename,
        "filesize": len(file_content)
    }) + "\n"

    data_to_send = header.encode("utf-8") + file_content # Combine header and file content before sending

    logging.info("Connecting to QUIC server on 127.0.0.1:4433")
    async with connect("10.10.20.5", 4433, configuration=configuration) as connection:

        logging.info("Connected to QUIC server")

        stream_id = connection._quic.get_next_available_stream_id() # Open a new stream and send the file.
        connection._quic.send_stream_data(stream_id, data_to_send, end_stream=True)

        logging.info("File sent on stream %d. Waiting for server to process...", stream_id)

        await asyncio.sleep(60) # Wait for server to receive and process, can increase if necessary

if __name__ == '__main__':
    time.sleep(5)
    asyncio.run(main())
