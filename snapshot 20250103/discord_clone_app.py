import customtkinter as ctk
import ctypes
import os
from PIL import Image
import pywinstyles
import mysql.connector
import sys
import socket
import sys
import errno
import threading

#username='bravo7313'
username=sys.argv[1]

HEADER_LENGTH=10
IP="192.168.29.4"
PORT=5050
FORMAT="utf-8"

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

socket_username=f"[{username}".encode(FORMAT)
socket_username_header = f"{len(socket_username):<{HEADER_LENGTH}}".encode(FORMAT)
client_socket.send(socket_username_header + socket_username)

mydb = mysql.connector.connect(
    host="localhost",
    user = "python",
    password = "9406817179!As",
    database = "discord_clone"
)
mycursor=mydb.cursor()

if '@' in username:
    mycursor.execute(f"select username from user_login_data where email = '{username}'")
    result=mycursor.fetchall()
    username=result[0][0]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

ctk.set_appearance_mode('System')
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        global friend_main_frame, friend_button, shop_button, nitro_button, fonts

        thread=threading.Thread(target=self.recvfunc)
        thread.start()

        fonts=self.font_family()
        images=self.images()

        self.geometry("{}x{}+0+0".format(screensize[0],screensize[1]))
        self.title("Discord Clone")
        self.iconbitmap(".\\Images\\DiscordIcon.ico")


        #name_list
        list_main_frame=ctk.CTkFrame(master=self, width=150,height=200,bg_color="#000001",fg_color="#2b2d31",corner_radius=10)
        list_main_frame.place(x=150,y=5)
        list_main_frame.grid_propagate(False)
        pywinstyles.set_opacity(list_main_frame,color="#000001")

        #friend,nitro,shop,search
        search_entry=ctk.CTkEntry(master=list_main_frame, placeholder_text="Search Friends")
        search_entry.grid(row = 0, column = 0, pady = 5)

        friend_button=ctk.CTkButton(master=list_main_frame,text="F R I E N D",font=fonts[0], anchor='w',image=images[0],compound="left",fg_color=("#2b2d31","#2b2d31"),bg_color=("#2b2d31","#2b2d31"),width=150,height=30,hover_color="#35373C",command=self.friend_func)
        friend_button.grid(row = 1, column = 0, pady = 5)

        nitro_button=ctk.CTkButton(master=list_main_frame,text="N I T R O",font=fonts[0], anchor='w',image=images[1],compound="left",fg_color=("#2b2d31","#2b2d31"),bg_color=("#2b2d31","#2b2d31"),width=150,height=30,hover_color="#35373C",command=self.nitro_func)
        nitro_button.grid(row = 2, column = 0, pady = 5)

        shop_button=ctk.CTkButton(master=list_main_frame,text="S H O P",font=fonts[0], anchor='w',image=images[2],compound="left",fg_color=("#2b2d31","#2b2d31"),bg_color=("#2b2d31","#2b2d31"),width=150,height=30,hover_color="#35373C",command=self.shop_func)
        shop_button.grid(row = 3, column = 0, pady = 5)

        end_line_label=ctk.CTkLabel(master=list_main_frame,text="_______________________",text_color="#02cef2")
        end_line_label.grid(row = 4, column = 0)

        friend_main_frame=ctk.CTkFrame(master=self, width=150, height=screensize[1]-300,bg_color='#000001',fg_color="#2b2b31",corner_radius=10)
        friend_main_frame.grid_propagate(False)
        pywinstyles.set_opacity(friend_main_frame,color="#000001")


    #friend,nitro,shop function
    def friend_func(self):
        global chat_main_frame, chat_box, message_entry, send_button

        friend_main_frame.place(x=150,y=210)
        friend_button.configure(fg_color="#404249")
        shop_button.configure(fg_color="#2b2b31")
        nitro_button.configure(fg_color="#2b2b31")

        direct_messages=ctk.CTkLabel(master=friend_main_frame, text="Direct Message",anchor = 'w')
        direct_messages.grid(row = 0, column = 0, pady=(5,0))

        mycursor.execute("select username from user_login_data")
        user_name_list=mycursor.fetchall()

        friend_name_button_dict={}

        for i in range(len(user_name_list)):
            if user_name_list[i][0]==username:
                continue
            def temp_func(clientusername=user_name_list[i][0]):
                return self.friend_chat_func(clientusername)
            friend_name_button_dict[user_name_list[i][0]]=ctk.CTkButton(master=friend_main_frame, text=user_name_list[i][0], anchor = 'w', fg_color=("#2b2b31","#2b2b31"),bg_color=("#2b2b31","#2b2b31"),hover_color="#35373C",command=temp_func)
            friend_name_button_dict[user_name_list[i][0]].grid(row=i+1,column=0,pady=(5,0))
        
        chat_main_frame=ctk.CTkFrame(master=self, width=1200, height=990,bg_color='#000001',fg_color='#2b2b31',corner_radius=10)
        chat_main_frame.place(x=310,y=5)
        chat_main_frame.grid_propagate(False)
        pywinstyles.set_opacity(chat_main_frame,color='#000001')

        chat_box=ctk.CTkTextbox(master=chat_main_frame,width=1200,height=1030,font=fonts[1],state="disabled")

        message_entry=ctk.CTkEntry(master=chat_main_frame, placeholder_text="Enter text", width=1000)

        send_button=ctk.CTkButton(master=chat_main_frame,text="send",command=lambda:self.sendfunc(client_user_name))

    def nitro_func(self):
        nitro_button.configure(fg_color="#404249")
        friend_button.configure(fg_color="#2b2b31")
        shop_button.configure(fg_color="#2b2b31")
    def shop_func(self):
        shop_button.configure(fg_color="#404249")
        friend_button.configure(fg_color="#2b2b31")
        nitro_button.configure(fg_color="#2b2b31")

    def friend_chat_func(self,clientusername):

        global client_user_name
        client_user_name=clientusername

        chat_main_frame.place(x=310,y=5)

        chat_box.grid(row=0, column=0)

        message_entry.place(x=10,y=950)

        send_button.place(x=1030,y=950)
    
    def sendfunc(self,client_user_name):
        message=f"To {client_user_name}] : {message_entry.get()}"

        if message:
            message = message.encode(FORMAT)
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode(FORMAT)

            client_socket.send(message_header + message)
            chat_box.configure(state='normal')
            chat_box.insert('end',f'[{username} {message.decode(FORMAT)}\n\n')
            chat_box.configure(state='disable')

    def recvfunc(self):
        while True:
            try:
                while True:
                    username_header = client_socket.recv(HEADER_LENGTH)

                    if not len(username_header):
                        chat_box.configure(state='normal')
                        chat_box.insert('end','Connection closed by server\n\n')
                        chat_box.configure(state='disable')
                        sys.exit()
                    username_length=int(username_header.decode(FORMAT).strip())

                    username = client_socket.recv(username_length).decode(FORMAT)

                    message_header = client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode(FORMAT).strip())
                    message = client_socket.recv(message_length).decode(FORMAT)

                    chat_box.configure(state='normal')
                    chat_box.insert('end',f'{username} > {message}\n\n')
                    chat_box.configure(state='disable')

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    chat_box.configure(state='normal')
                    chat_box.insert('end','Reading error: {}\n\n'.format(str(e)))
                    chat_box.configure(state='disable')
                    sys.exit()
                continue
            except Exception as e:
                chat_box.configure(state='normal')
                chat_box.insert("end","Reading error: {}\n\n".format(str(e)))
                chat_box.configure(state='disable')
                sys.exit()

    def font_family(self):
        #index 0
        friend_font=ctk.CTkFont(family="Alphacorsa Personal Use",size=12)
        chat_font=ctk.CTkFont(family="Roboto", size=20)
        return [friend_font,chat_font]

    def images(self):
        #index 0
        friend_icon=ctk.CTkImage(light_image=Image.open(".\\Images\\friend_icon.png"),
                                 dark_image=Image.open(".\\Images\\friend_icon.png"),
                                 size=(18,15))

        #index 1
        nitro_icon=ctk.CTkImage(light_image=Image.open(".\\Images\\nitro_icon.png"),
                                 dark_image=Image.open(".\\Images\\nitro_icon.png"),
                                 size=(18,15))

        #index 2
        shop_icon=ctk.CTkImage(light_image=Image.open(".\\Images\\shop_icon.png"),
                                 dark_image=Image.open(".\\Images\\shop_icon.png"),
                                 size=(18,15))
        return [friend_icon,nitro_icon,shop_icon]

if __name__=="__main__":
    app = App()
    app.mainloop()
