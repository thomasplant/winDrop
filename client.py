import socket
import tkinter as tk
from tkinter import filedialog, scrolledtext

if __name__ == "__main__":

    host = '127.0.0.1'
    port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4, TCP)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (IPv4, UDP)
    sock.connect((host,port))

    # File transfer
    while True:
        filename = input('Input filename you want to transfer: ')

        try:
            file = open(filename, 'r')
            data = file.read()
            if not data:
                break
            while data:
                sock.send(str(data).encode())
                data = file.read()
            file.close()

        except IOError as error:
            print("Error: Invalid filename or can not open file! Please try again!")
            print("Debug log: ", error)