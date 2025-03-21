from CTkScrollableDropdown import *
import customtkinter as ctk
import ctypes
from PIL import Image
import random
import datetime
import pywinstyles
from functools import partial
import os
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import awesometkinter as atk
import threading
import time as t

mydb = mysql.connector.connect(
    host = "localhost",
    user = "python",
    password = "9406817179!As",
    port=3306,
    database="discord_clone")
mycursor = mydb.cursor()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        global fonts, images, login_name_entry, login_password_entry,mail_error,password_error

        self.database_check_func()

        self.title("Discord")
        self.geometry(f"{screensize[0]}x{screensize[1]}+0+0")
        self.wm_iconbitmap(bitmap=".\\Images\\DiscordIcon.ico")

        images=self.images_func()
        fonts=self.fonts_func()


        background_image_label=ctk.CTkLabel(master=self, image=images[0],text="", width=screensize[0],height=screensize[1])
        background_image_label.place(x=0,y=0)

        discord_image_frame=ctk.CTkFrame(master=self,width=220,height=45,corner_radius=20,bg_color=("#000001","#000001"))
        discord_image_frame.place(x=-20,y=70)
        pywinstyles.set_opacity(discord_image_frame, color="#000001")

        discord_image_label=ctk.CTkLabel(master=discord_image_frame, image=images[1],text="Discord", width=150,compound='left',font=fonts[0],bg_color="#000001")
        discord_image_label.place(x=50,y=10)
        pywinstyles.set_opacity(discord_image_label, color="#000001")

        main_frame=ctk.CTkFrame(master=self,width=screensize[0]/3,height=screensize[1]/2,bg_color='#000001',corner_radius=20)
        main_frame.place(x=screensize[0]/3,y=screensize[1]/4)
        main_frame.grid_propagate(False)
        main_frame.grid_columnconfigure((1), weight=1)
        pywinstyles.set_opacity(main_frame,color="#000001")


        welcome_label=ctk.CTkLabel(master=main_frame, text="Welcome!", font=fonts[1])
        welcome_label.grid(row=0,column=1,columnspan=3,pady=(50,30),padx=(0,50),sticky='we')

        message_label=ctk.CTkLabel(master=main_frame, text="We're so excited to see you!",text_color="grey")
        message_label.grid(row=1,column=1,columnspan=3,padx=(0,50),sticky='we')

        login_name_label=ctk.CTkLabel(master=main_frame, text="UserName/Email:")
        login_name_label.grid(row=2,column=0,pady=(40,5),padx=(50,0))

        login_name_entry=ctk.CTkEntry(master=main_frame, placeholder_text="UserName or email", width=(screensize[0]/3)-100,height=30, corner_radius=10)
        login_name_entry.grid(row=2,column=1,pady=(40,5),padx=(5,50),columnspan=3,sticky='we')

        login_password_label=ctk.CTkLabel(master=main_frame, text="Password:")
        login_password_label.grid(row=4,column=0,pady=(35,5),padx=(50,0))

        login_password_entry=ctk.CTkEntry(master=main_frame, placeholder_text="Secure Password", width=(screensize[0]/3)-100,height=30, corner_radius=10,show='*')
        login_password_entry.grid(row=4,column=1,pady=(35,5),padx=(5,50),columnspan=3,sticky='we')

        login_button=ctk.CTkButton(master=main_frame, text="Login", corner_radius=10, command=self.login_func)
        login_button.grid(row=6,column=1,pady=35,padx=(0,50),columnspan=3,sticky='we')

        forget_password_button=ctk.CTkButton(master=main_frame,text="Forget Password", bg_color='#2B2B2B',fg_color='#2B2B2B',hover_color="#2B2B2B",text_color='#6FCFEB',command=self.forget_password_func)
        forget_password_button.grid(row=7,column=1,padx=(0,50),columnspan=3,sticky='we')
        forget_password_button.bind("<Enter>", partial(self.hover_config_func, forget_password_button, "white"))
        forget_password_button.bind("<Leave>", partial(self.hover_config_func, forget_password_button, "#6FCFEB"))

        register_button=ctk.CTkButton(master=main_frame, text="Register Now", bg_color='#2B2B2B',fg_color='#2B2B2B',hover_color="#2B2B2B",text_color='#6FCFEB',command=self.register_func)
        register_button.grid(row=8,column=1,padx=(0,50),columnspan=3,sticky='we')
        register_button.bind("<Enter>", partial(self.hover_config_func, register_button, "white"))
        register_button.bind("<Leave>", partial(self.hover_config_func, register_button, "#6FCFEB"))

        mail_error=ctk.CTkLabel(master=main_frame, text="Invaild Mail",text_color="red")
        password_error=ctk.CTkLabel(master=main_frame, text="Incorrect Password", text_color="red")

    def login_func(self):
        username=login_name_entry.get()
        password=login_password_entry.get()

        mycursor.execute("select email,password,username from user_login_data")
        user_id_list=mycursor.fetchall()
        for i in range(len(user_id_list)):
            if (username==user_id_list[i][0]) or (username==user_id_list[i][2]):
                mail_error.grid_forget()
                if password==user_id_list[i][1]:
                    password_error.grid_forget()
                    os.system(f'start discord_clone_app.py "{username}"')
                    exit()
                else:
                    password_error.grid(row=5,column=1,pady=(35,5),padx=(5,50),columnspan=3,sticky='we')
            else:
                mail_error.grid(row=3,column=1,pady=(35,5),padx=(5,50),columnspan=3,sticky='we')
        
    

    def background_random_images_func(self):
        image_name_list=[0,1,2,3,4]
        current_date = datetime.datetime.now()
        random.seed(int(current_date.strftime("%Y%m%d%H%M%S")))
        i=random.choice(image_name_list)
        return i

    def images_func(self):
        i=self.background_random_images_func()

        #index 0
        background_image=ctk.CTkImage(light_image=Image.open(f"Images\\Saved Pictures\\{i}.png"),
                                dark_image=Image.open(f"Images\\Saved Pictures\\{i}.png"),
                                size=(screensize[0],screensize[1]))

        #index 1
        discord_image=ctk.CTkImage(light_image=Image.open("Images\\discord_icon.png"),
                                   dark_image=Image.open("Images\\discord_icon.png"),
                                   size=(30,30))
        return [background_image,discord_image]

    def fonts_func(self):
        #Index 0
        discord_logo_font=ctk.CTkFont(family="Alphacorsa Personal Use", size=18)

        #Index 1
        welcome_font=ctk.CTkFont(family="Arial Black",size=25)

        #Index 2
        message_font=ctk.CTkFont(family="Berlin Sans FB Demi",size=18)

        return [discord_logo_font,welcome_font,message_font]


    def hover_config_func(self,widget,color,event):
        widget.configure(text_color=color)

    def forget_password_func(self):
        global user_email_forget_entry, next_button,back_frame, change_frame,no_mail_error_label,user_email_forget_label
        
        back_frame=ctk.CTkFrame(master=self,width=screensize[0],height=screensize[1],fg_color='#000001',bg_color='#000001')
        back_frame.place(x=0,y=0)
        pywinstyles.set_opacity(back_frame,value=0.5)
        back_frame.pack_propagate(False)

        change_frame=ctk.CTkFrame(master=self, width=480,height=320,corner_radius=20,bg_color='#000001')
        change_frame.pack(pady=(380,0))
        pywinstyles.set_opacity(change_frame,color='#000001')
        change_frame.pack_propagate(False)

        started_label=ctk.CTkLabel(master=change_frame, text="Forget Something?", font=fonts[1])
        started_label.place(x=120,y=50)

        user_email_forget_label=ctk.CTkLabel(master=change_frame,text="Email:")
        user_email_forget_label.place(x=50,y=150)
        user_email_forget_entry=ctk.CTkEntry(master=change_frame, placeholder_text="discord@gmail.com", width=320)
        user_email_forget_entry.place(x=120,y=150)

        next_button=ctk.CTkButton(master=change_frame, text="Next", corner_radius=10, command=self.mail_check_func)
        next_button.place(x=180, y=280)

        close_button=ctk.CTkButton(master=change_frame, text="X", bg_color='#2B2B2B',fg_color='#2B2B2B',hover_color="#2B2B2B",text_color='grey',width=5 ,command=self.close_forget_panel_func)
        close_button.place(x=450, y=8)
        close_button.bind("<Enter>", partial(self.hover_config_func, close_button, "white"))
        close_button.bind("<Leave>", partial(self.hover_config_func, close_button, "grey"))

        no_mail_error_label=ctk.CTkLabel(master=change_frame,text='Invaild Mail',text_color='red')
        #grid.grid(self)

    def mail_check_func(self):
        global user_email
        # mail check part

        user_email=user_email_forget_entry.get()

        mycursor.execute("select email from user_login_data")
        user_email_list=mycursor.fetchall()
        if not user_email.lower()in user_email_list[0][0]:
               no_mail_error_label.place(x=230,y=180)
        else:
            no_mail_error_label.destroy()
            self.update_idletasks()
            user_email_forget_entry.configure(state= "disabled",text_color='grey')
            self.otp_func()

    def otp_func(self):
        global otp, otp_entry, incorrect_otp_label, otp_label
        
        # OPT part       
        current_date = datetime.datetime.now()
        random.seed(int(current_date.strftime("%Y%m%d%H%M%S")))
        num_list=[0,1,2,3,4,5,6,7,8,9]
        otp=''
        for i in range(6):
            otp+=str(random.choice(num_list))

        otp_label=ctk.CTkLabel(master=change_frame, text="OTP: ")
        otp_label.place(x=50,y=200)
        otp_entry=ctk.CTkEntry(master=change_frame, placeholder_text="OTP", width=320)
        otp_entry.place(x=120,y=200)

        next_button.configure(command=self.otp_check_func)

        incorrect_otp_label=ctk.CTkLabel(master=change_frame,text="Invaild OTP",text_color='red')

        self.update_idletasks()
        t1=threading.Thread(target=self.loading_func)
        t2=threading.Thread(target=self.otp_send_func)
        t1.start()
        t2.start()

    def loading_func(self):
        main_frame=ctk.CTkFrame(master=change_frame,corner_radius=20,bg_color='#000001',width=480,height=320)
        main_frame.place(x=0,y=0)
        main_frame.pack_propagate(False)
        pywinstyles.set_opacity(main_frame,value=0.5)
        process_bar=atk.RadialProgressbar3d(change_frame,fg="green",parent_bg="#2B2B2B",size=(130,130))
        process_bar.pack(pady=(100,0))
        process_bar.set(0)
        for i in range(11):
            j=i*10
            process_bar.set(j)
            self.update_idletasks()
            t.sleep(0.5)
        process_bar.destroy()
        main_frame.destroy()
        

    def otp_check_func(self):
        user_otp=otp_entry.get()

        if not user_otp==otp:
            incorrect_otp_label.place(x=230,y=230)
        else:
            incorrect_otp_label.destroy()
            self.change_password_func()

    def change_password_func(self):
        global new_password_entry, comfirm_password_entry,strong_password_error
        
        otp_entry.destroy()
        otp_label.destroy()
        user_email_forget_label.destroy()
        user_email_forget_entry.destroy()

        new_password_label=ctk.CTkLabel(master=change_frame,text="New Password")
        new_password_label.place(x=50,y=100)
        new_password_entry=ctk.CTkEntry(master=change_frame,placeholder_text="New Password",width=390)
        new_password_entry.place(x=50,y=130)

        comfirm_password_label=ctk.CTkLabel(master=change_frame, text="Comfirm Password")
        comfirm_password_label.place(x=50,y=180)
        comfirm_password_entry=ctk.CTkEntry(master=change_frame, placeholder_text="Comfirm Password", width=390)
        comfirm_password_entry.place(x=50,y=210)

        strong_password_error=ctk.CTkLabel(master=change_frame,text="Password should contain 'Regular Aplhabat', 'Capital Alphabat', 'Numbers' and  'Symbols'",text_color='red')

        next_button.configure(text="Change",command=self.comfirm_change_password_func)

    def comfirm_change_password_func(self):
        new_password=new_password_entry.get()
        comfirm_password=comfirm_password_entry.get()
        
        password_list=[]
        for i in new_password:
            password_list.append(i)
        small_letter_list=[]
        for i in range(97,123):
            small_letter_list.append(chr(i))

        big_letter_list=[]
        for i in range(65,91):
            big_letter_list.append(chr(i))

        number_list=['0','1','2','3','4','5','6','7','8','9']
        symbol_list=[]
        for i in range(33,48):
            symbol_list.append(chr(i))
        for i in range(58,65):
            symbol_list.append(chr(i))
        for i in range(91,97):
            symbol_list.append(chr(i))
        for i in range(123,127):
            symbol_list.append(chr(i))
        small_letter_set=set(small_letter_list)
        big_letter_set=set(big_letter_list)
        number_set=set(number_list)
        symbol_set=set(symbol_list)
        password_set=set(password_list)

        checklist1=small_letter_set.intersection(password_set)
        checklist2=big_letter_set.intersection(password_set)
        checklist3=number_set.intersection(password_set)
        checklist4=symbol_set.intersection(password_set)

        mycursor.execute("select email,password from user_login_data")
        user_id_list=mycursor.fetchall()

        for i in range(len(user_id_list)):
            if user_email==user_id_list[i][0]:
                user_password=user_id_list[i][1]  

        if len(new_password)<8:
            strong_password_error.configure(text="Password Should have atleast 8 characters")
            strong_password_error.pack(pady=(250,0))
            self.update_idletasks()
        elif new_password!=comfirm_password:
            strong_password_error.configure(text="Password just not match")
            strong_password_error.pack(pady=(250,0))
            self.update_idletasks()
        elif (len(checklist1)==0) or (len(checklist2)==0) or (len(checklist3)==0) or (len(checklist4)==0):
            strong_password_error.configure(text="Password must contain 'Captial Letter', 'Regular Letter', 'Numbers' and 'Symbols'")
            strong_password_error.pack(pady=(250,0))
            self.update_idletasks()
        elif new_password==user_password:
                    strong_password_error.configure(text="Password cannot be same as last password")
                    strong_password_error.pack(pady=(250,0))
                    self.update_idletasks()     
        else:
            strong_password_error.destroy()

            mycursor.execute(f"UPDATE user_login_data SET password='{new_password}' WHERE email = '{user_email}'")

            mydb.commit()
            
            for widgets in change_frame.winfo_children():
                widgets.destroy()
            successfull_label=ctk.CTkLabel(master=change_frame, text="Successfull", font=fonts[1])
            successfull_label.pack(pady=140)

            close_button=ctk.CTkButton(master=change_frame, text="X", bg_color='#2B2B2B',fg_color='#2B2B2B',hover_color="#2B2B2B",text_color='grey',width=5 ,command=self.close_forget_panel_func)
            close_button.place(x=450, y=8)
            close_button.bind("<Enter>", partial(self.hover_config_func, close_button, "white"))
            close_button.bind("<Leave>", partial(self.hover_config_func, close_button, "grey"))
        

    def otp_send_func(self):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("testservermail7@gmail.com","poft zgfg cilj bzud")

        message=MIMEMultipart()
        message['From']="testservermail7@gmail.com"
        message['To']=user_email
        message['Subject']="NO REPLY, OTP FOR DISCORD CLONE"

        message_body=f"Your OTP for Discord Clone is {otp}"

        message.attach(MIMEText(message_body,'plain'))

        msg=message.as_string()

        s.sendmail("testservermail7@gmail.com",user_email,msg)

        s.quit()
        

    def database_check_func(self):
        mycursor.execute("show tables")
        table_list_pointer=mycursor.fetchall()

        table_list=[]
        for i in range(len(table_list_pointer)):
            table_list.append(table_list_pointer[0][i])
        
        if "user_login_data" not in table_list:
            current_time=datetime.datetime.now()
            mycursor.execute("create table user_login_data(email char(50),password char(50),username char(50))")
            mydb.commit()
            target=open("logs.txt","a")
            target.write(f"{current_time}: User Login Table not found 'user_login_data not found';\n{current_time}: Creating a new database 'user_login_data'")

    def close_forget_panel_func(self):
        for widgets in change_frame.winfo_children():
            widgets.destroy()
        back_frame.destroy()
        change_frame.destroy()

    
    def register_func(self):
        global register_frame, back_frame, user_email_entry,user_name_entry, user_password_entry, day_combo,month_combo,year_combo,strong_password_error,email_exist_error,username_exist_error,invaild_mail_error
        
        back_frame=ctk.CTkFrame(master=self,width=screensize[0],height=screensize[1],fg_color='#000001',bg_color='#000001')
        back_frame.place(x=0,y=0)
        pywinstyles.set_opacity(back_frame,value=0.5)
        back_frame.pack_propagate(False)

        register_frame_height=520
        register_frame=ctk.CTkFrame(master=self, width=480,height=register_frame_height,corner_radius=20,bg_color='#000001')
        register_frame.pack(pady=((screensize[1]/2)-(register_frame_height/2),0))
        pywinstyles.set_opacity(register_frame,color='#000001')
        register_frame.pack_propagate(False)

        started_label=ctk.CTkLabel(master=register_frame, text="Let's Get Started", font=fonts[1])
        started_label.place(x=120,y=50)

        user_email_label=ctk.CTkLabel(master=register_frame,text="Email:")
        user_email_label.place(x=50,y=120)
        user_email_entry=ctk.CTkEntry(master=register_frame,placeholder_text="discord@gmail.com",width=380)
        user_email_entry.place(x=50,y=150)

        user_name_label=ctk.CTkLabel(master=register_frame,text="UserName:")
        user_name_label.place(x=50,y=200)
        user_name_entry=ctk.CTkEntry(master=register_frame, placeholder_text="UserName", width=380)
        user_name_entry.place(x=50,y=230)

        user_password_label=ctk.CTkLabel(master=register_frame,text="Password:")
        user_password_label.place(x=50,y=280)
        user_password_entry=ctk.CTkEntry(master=register_frame, placeholder_text="secure Password", width=380,show='*')
        user_password_entry.place(x=50,y=310)

        current_date = datetime.datetime.now()
        day=[]
        month=[]
        year=[]
        for i in range(1,32):
            day.append(str(i))
        for i in range(1,13):
            month.append(str(i))
        for i in range(1900,int(current_date.strftime("%Y"))+1):
            year.append(str(i))
        
        date_of_birth_label=ctk.CTkLabel(master=register_frame, text="Date of Birth")
        date_of_birth_label.place(x=50,y=370)
        
        day_combo=ctk.CTkComboBox(master=register_frame,width=100)
        day_combo.place(x=63,y=400)
        CTkScrollableDropdown(day_combo, values=day, justify="left", button_color="transparent")
        day_combo.set('1')
        
        month_combo=ctk.CTkComboBox(master=register_frame,width=100)
        month_combo.place(x=189,y=400)
        CTkScrollableDropdown(month_combo, values=month, justify="left", button_color="transparent")
        month_combo.set('1')

        year_combo=ctk.CTkComboBox(master=register_frame,width=100)
        year_combo.place(x=315,y=400)
        CTkScrollableDropdown(year_combo, values=year, justify="left", button_color="transparent")
        year_combo.set("2000")

        register_comfirm_button=ctk.CTkButton(master=register_frame, text="Register", corner_radius=10, command=self.register_comfirm_func)
        register_comfirm_button.place(x=180,y=470)

        close_button=ctk.CTkButton(master=register_frame, text="X", bg_color='#2B2B2B',fg_color='#2B2B2B',hover_color="#2B2B2B",text_color='grey',width=5 ,command=self.close_register_panel_func)
        close_button.place(x=450, y=8)
        close_button.bind("<Enter>", partial(self.hover_config_func, close_button, "white"))
        close_button.bind("<Leave>", partial(self.hover_config_func, close_button, "grey"))

        strong_password_error=ctk.CTkLabel(master=register_frame,text="Password should contain 'Regular Aplhabat', 'Capital Alphabat', 'Numbers' and  'Symbols'",text_color='red')
        email_exist_error=ctk.CTkLabel(master=register_frame,text="Email ID Already exist",text_color='red')
        username_exist_error=ctk.CTkLabel(master=register_frame,text="Username already taken",text_color='red')
        invaild_mail_error=ctk.CTkLabel(master=register_frame,text="Invaild Email Address",text_color='red')

    def register_comfirm_func(self):
        global user_email, user_name, user_password, user_dob
        day=day_combo.get()
        month=month_combo.get()
        year=year_combo.get()
        user_dob=year+'-'+month+'-'+day
        user_email=user_email_entry.get().lower()
        user_name=user_name_entry.get().lower()
        user_password=user_password_entry.get()

        
        password_list=[]
        for i in user_password:
            password_list.append(i)
        small_letter_list=[]
        for i in range(97,123):
            small_letter_list.append(chr(i))

        big_letter_list=[]
        for i in range(65,91):
            big_letter_list.append(chr(i))

        number_list=['0','1','2','3','4','5','6','7','8','9']
        symbol_list=[]
        for i in range(33,48):
            symbol_list.append(chr(i))
        for i in range(58,65):
            symbol_list.append(chr(i))
        for i in range(91,97):
            symbol_list.append(chr(i))
        for i in range(123,127):
            symbol_list.append(chr(i))
        small_letter_set=set(small_letter_list)
        big_letter_set=set(big_letter_list)
        number_set=set(number_list)
        symbol_set=set(symbol_list)
        password_set=set(password_list)

        checklist1=small_letter_set.intersection(password_set)
        checklist2=big_letter_set.intersection(password_set)
        checklist3=number_set.intersection(password_set)
        checklist4=symbol_set.intersection(password_set)
        


        if len(user_password)<8:
            strong_password_error.configure(text="Password Should have atleast 8 characters")
            strong_password_error.place(x=50,y=340)
            check1=False
        elif (len(checklist1)==0) or (len(checklist2)==0) or (len(checklist3)==0) or (len(checklist4)==0):
            strong_password_error.configure(text="Password must contain 'Captial Letter', 'Regular Letter', 'Numbers' and 'Symbols'")
            strong_password_error.place(x=50,y=340)
            check1=False
        else:
            strong_password_error.destroy()
            check1=True


        mycursor.execute("select email,username from user_login_data")
        user_id_list=mycursor.fetchall()

        user_email_list=[]
        user_name_list=[]
        for i in range(len(user_id_list)):
                user_email_list.append(user_id_list[i][0])
                user_name_list.append(user_id_list[i][1])

        templist=[]
        for i in range(len(user_email)):
            templist.append(user_email[i])
        if not '@' in templist:
            invaild_mail_error.place(x=50,y=180)
            check2=False
        else:
            invaild_mail_error.place_forget()
            check2=True
                    
                    
        if user_email.lower() in user_email_list:
            email_exist_error.place(x=50,y=180)
            check3=False
        else:
            email_exist_error.place_forget()
            self.update_idletasks()
            check3=True

                    
        if user_name.lower()in user_name_list:
            username_exist_error.place(x=50,y=260)
            check4=False
        else:
            username_exist_error.place_forget()
            self.update_idletasks()
            check4=True
        
        if (check1==True) and (check2==True) and (check3==True) and (check4==True):
            for widgets in register_frame.winfo_children():
                widgets.destroy()
            back_frame.destroy()
            register_frame.destroy()
            self.otp_func2()
            
    def otp_func2(self):
        global otp, otp_entry, incorrect_otp_label, otp_label,main_frame,next_button
        
        # OPT part       
        current_date = datetime.datetime.now()
        random.seed(int(current_date.strftime("%Y%m%d%H%M%S")))
        num_list=[0,1,2,3,4,5,6,7,8,9]
        otp=''
        for i in range(6):
            otp+=str(random.choice(num_list))

        main_frame=ctk.CTkFrame(master=self,corner_radius=20,width=480,height=320)
        main_frame.pack(pady=((screensize[1]/2)-160))
        main_frame.pack_propagate(False)

        otp_label=ctk.CTkLabel(master=main_frame, text="OTP: ",font=fonts[1])
        otp_label.pack(pady=(30,0))
        otp_entry=ctk.CTkEntry(master=main_frame, placeholder_text="OTP", width=320)
        otp_entry.pack(pady=(70,0))
        
        incorrect_otp_label=ctk.CTkLabel(master=main_frame,text="Invaild OTP",text_color='red')

        next_button=ctk.CTkButton(master=main_frame, text="Next", corner_radius=10, command=self.otp_check_func2)
        next_button.pack(pady=(50,0))

        close_button=ctk.CTkButton(master=main_frame, text="X", bg_color='#2B2B2B',fg_color='#2B2B2B',hover_color="#2B2B2B",text_color='grey',width=5 ,command=self.close_otp_panel_func)
        close_button.place(x=450, y=8)
        close_button.bind("<Enter>", partial(self.hover_config_func, close_button, "white"))
        close_button.bind("<Leave>", partial(self.hover_config_func, close_button, "grey"))

        self.update_idletasks()
        
        self.otp_send_func()

    def otp_check_func2(self):
        user_otp=otp_entry.get()

        if user_otp != otp:
            incorrect_otp_label.pack(pady=(30,0))
        else:
            incorrect_otp_label.destroy()
            

            mycursor.execute(f"INSERT INTO user_login_data VALUES('{user_email}','{user_password}','{user_name}','{user_dob}')")
            mydb.commit()

            next_button.destroy()
            otp_entry.destroy()
            back_frame.destroy()

            otp_label.configure(text="Success Full")
            otp_label.pack(pady=(120,0))

        

    def close_register_panel_func(self):
        for widgets in register_frame.winfo_children():
            widgets.destroy()
        back_frame.destroy()
        register_frame.destroy()

    def close_otp_panel_func(self):
        for widgets in main_frame.winfo_children():
            widgets.destroy()
        back_frame.destroy()
        main_frame.destroy()

if __name__=="__main__":
    app=App()
    app.mainloop()