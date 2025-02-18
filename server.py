import socket
import tkinter as tk
from tkinter import filedialog, scrolledtext

if __name__ == "__main__":
    # Socket parameters

    host = "127.0.0.1"
    port = 8080
    totalClients = int(input("Enter number of clients: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4, TCP)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (IPv4, UDP)
    sock.bind((host, port))
    sock.listen(totalClients)
    connections = []
    print("Initiating clients")


    for i in range(totalClients):
        conn = sock.accept()
        connections.append(conn) # Stores into connections list
        print("connected with client", i + 1)

    fileno = 0
    index = 0 

    for conn in connections:
        index = index + 1
        data = conn[0].recv(1024).decode()
        if not data:
            continue
        filename = 'output'+str(fileno)+'.txt'
        fileno = fileno + 1
        fileopen = open(filename, 'w')
        while data:
            if not data:
                break
            else:
                fileopen.write(data)
                data = conn[0].recv(1024).decode()
        print()
        print('Receiving file from client', index)
        print()
        print('Received succesfully! New filename is: ', filename)
        fileopen.close()

    # Closing connections
    for con in connections:
        conn[0].close()
