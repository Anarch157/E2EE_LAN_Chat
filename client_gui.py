import socket
import threading
from time import sleep
from tkinter import *
from tkinter import scrolledtext

win = Tk()
win.geometry('600x400')
win.config(background="#300000")
win.title("Client")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_field = Entry(win, background="#413109", foreground="#ffffff", font=14)
ip_field.grid(row=0, column=0)

ip_label = Label(win, text="server ip", background="#300000", foreground="#ffffff", font=14)
ip_label.grid(row=1, column=0)

port_field = Entry(win, background="#413109", foreground="#ffffff", font=14)
port_field.grid(row=0, column=1)

port_label = Label(win, text="server port", background="#300000", foreground="#ffffff", font=14)
port_label.grid(row=1, column=1)

text_box = scrolledtext.ScrolledText(win, width=50, height=10, background="#413109", foreground="#ffffff", font=14)
text_box.grid(row=2, column=0, columnspan=3)
text_box.config(state="disabled")

empty_label = Label(win, text="", background="#300000", foreground="#ffffff", font=14)
empty_label.grid(row=3, column=0)

send_field = Entry(win, width=40, background="#413109", foreground="#ffffff", font=14)
send_field.grid(row=4, column=0, columnspan=2)


def send():
    msg = send_field.get()
    s.send(bytes(msg, "ascii"))
    send_field.delete(0, 'end')


send_button = Button(win, text="send", command=send, background="#2f2f60", foreground="#ffffff", font=14)
send_button.grid(row=4, column=2)


def connect():
    s.connect((ip_field.get(), int(port_field.get())))

    def receive():
        while True:
            msg = s.recv(1024).decode("ascii")
            text_box.config(state="normal")
            text_box.insert('end', msg + '\n')
            text_box.config(state="disabled")
            text_box.yview('end')
            sleep(1)

    t1 = threading.Thread(target=receive)
    t1.start()


connect_button = Button(win, text="Connect", font=14, command=connect, background="#2f2f60", foreground="#ffffff")
connect_button.grid(row=0, column=2)

win.mainloop()
