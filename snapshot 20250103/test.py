import threading
import socket

IP="192.168.29.4"
PORT=5050

server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP,PORT))

server_socket.listen()

while True:
    client_socket, client_address = server_socket.accept()

       