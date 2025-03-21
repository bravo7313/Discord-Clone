import customtkinter as ctk
import pywinstyles

def grid(window):
    #app=window
    xaxis=0
    yaxis=0
    for i in range(0,1920,20):
        frame1=ctk.CTkFrame(master=window, width=20, height=1080, border_width=1,border_color="black")
        frame1.place(x=i,y=0)
        xaxis+=20
        pywinstyles.set_opacity(frame1,value=0.5)

        frame2=ctk.CTkFrame(master=window, width=1920, height=20, border_width=1,border_color="black")
        frame2.place(x=0,y=i)
        yaxis+=20
        pywinstyles.set_opacity(frame2,value=0.5)

        label1=ctk.CTkLabel(master=frame1, text=xaxis)
        label1.place(x=2,y=2)
        label2=ctk.CTkLabel(master=frame2, text=yaxis)
        label2.place(x=2,y=2)



