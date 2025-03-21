import socket
import customtkinter as ctk
import sys
import errno
import threading

ctk.set_appearance_mode('System')
ctk.set_default_color_theme("blue")
def socket_client_func(self,client_user_name,chat_box,message_entry):

    HEADER_LENGTH=10

    IP="192.168.29.4"
    PORT=5050
    FORMAT='utf-8'

    client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((IP,PORT))

    client_socket.setblocking(False)

    username=client_user_name.encode(FORMAT)
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode(FORMAT)

    client_socket.send(username_header + username)


    def sendfunc(self):
        message=message_entry.get()

        if message:
            message = message.encode(FORMAT)
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode(FORMAT)

            client_socket.send(message_header + message)
            chat_box.insert('end',f'{client_user_name} > {message}\n')
        
    def recvfunc(self):
        while True:
                
            try:
                while True:
                    username_header = client_socket.recv(HEADER_LENGTH)

                    if not len(username_header):
                        chat_box.insert('end','Connection closed by server\n')
                        sys.exit()
                    username_length=int(username_header.decode(FORMAT).strip())

                    username = client_socket.recv(username_length).decode(FORMAT)

                    message_header = client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode(FORMAT).strip())
                    message = client_socket.recv(message_length).decode(FORMAT)

                    chat_box.insert('end',f'{username} > {message}\n')

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    chat_box.insert('end','Reading error: {}\n'.format(str(e)))
                    sys.exit()
                continue
            except Exception as e:
                chat_box.insert("end","Reading error: {}\n".format(str(e)))
                sys.exit()

    thread=threading.Thread(target=recvfunc)
    thread.start()