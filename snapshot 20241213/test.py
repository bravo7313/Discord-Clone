import customtkinter as ctk
import ctypes
import os
from PIL import Image

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

ctk.set_appearance_mode('System')
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        fonts=self.font_family()
        images=self.images()

        self.geometry("{}x{}+0+0".format(screensize[0],screensize[1]))
        self.title("Discord Clone")
        self.iconbitmap(".\\Images\\DiscordIcon.ico")


        #name_list
        list_main_frame=ctk.CTkFrame(master=self, width=150,height=screensize[1]-60,bg_color="#2b2d31",fg_color="#2b2d31")
        list_main_frame.place(x=150,y=30)

        list_frame=ctk.CTkFrame(master=self, width=150,height=screensize[1]-60,bg_color="#2b2d31",fg_color="#2b2d31")
        list_frame.place(x=150,y=30)

        #friend,nitro,shop
        friend_button=ctk.CTkButton(master=list_frame,text="F R I E N D",font=fonts[0], anchor='w',image=images[0],compound="left",fg_color=("#2b2d31","#2b2d31"),bg_color=("#2b2d31","#2b2d31"),width=150,height=30,command=self.friend_func)
        friend_button.grid(row=0,column=0,pady = 5)

        nitro_button=ctk.CTkButton(master=list_frame,text="N I T R O",font=fonts[0], anchor='w',image=images[1],compound="left",fg_color=("#2b2d31","#2b2d31"),bg_color=("#2b2d31","#2b2d31"),width=150,height=30,command=self.nitro_func)
        nitro_button.grid(row=1,column=0,pady = 5)

        shop_button=ctk.CTkButton(master=list_frame,text="S H O P",font=fonts[0], anchor='w',image=images[2],compound="left",fg_color=("#2b2d31","#2b2d31"),bg_color=("#2b2d31","#2b2d31"),width=150,height=30,command=self.shop_func)
        shop_button.grid(row=2,column=0,pady = 5)


    #friend,nitro,shop function
    def friend_func(self):
        pass

    def nitro_func(self):
        pass

    def shop_func(self):
        pass

    #All font decalered here
    def font_family(self):
        #index 0
        friend_font=ctk.CTkFont(family="Alphacorsa Personal Use",size=12)
        return [friend_font]

    def images(self):
        #index 0
        friend_icon=ctk.CTkImage(light_image=Image.open("images\\friend_icon.png"),
                                 dark_image=Image.open("images\\friend_icon.png"),
                                 size=(18,15))

        #index 1
        nitro_icon=ctk.CTkImage(light_image=Image.open("images\\nitro_icon.png"),
                                 dark_image=Image.open("images\\nitro_icon.png"),
                                 size=(18,15))

        #index 2
        shop_icon=ctk.CTkImage(light_image=Image.open("images\\shop_icon.png"),
                                 dark_image=Image.open("images\\shop_icon.png"),
                                 size=(18,15))
        return [friend_icon,nitro_icon,shop_icon]

if __name__=="__main__":
    app = App()
    app.mainloop()
