import socket
import threading
from time import sleep
from tkinter import *
from tkinter import scrolledtext
from cryptography.fernet import Fernet

file = open('key.txt', 'rb')
key = file.read()
file.close()
f = Fernet(key)

win = Tk()
win.geometry('800x400')
win.config(background="#300000")
win.title("Client")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_field = Entry(win, background="#413109", foreground="#ffffff", font=14, width=15)
ip_field.grid(row=0, column=0)

ip_label = Label(win, text="server ip", background="#300000", foreground="#ffffff", font=14)
ip_label.grid(row=1, column=0)

port_field = Entry(win, background="#413109", foreground="#ffffff", font=14, width=15)
port_field.grid(row=0, column=1)

port_label = Label(win, text="server port", background="#300000", foreground="#ffffff", font=14)
port_label.grid(row=1, column=1)

name_field = Entry(win, background="#413109", foreground="#ffffff", font=14, width=15)
name_field.grid(row=0, column=2)

name_label = Label(win, text="name", background="#300000", foreground="#ffffff", font=14)
name_label.grid(row=1, column=2)

text_box = scrolledtext.ScrolledText(win, width=50, height=10, background="#413109", foreground="#ffffff", font=14)
text_box.grid(row=2, column=0, columnspan=3)
text_box.config(state="disabled")

empty_label = Label(win, text="", background="#300000", foreground="#ffffff", font=14)
empty_label.grid(row=3, column=0)

send_field = Entry(win, width=40, background="#413109", foreground="#ffffff", font=14)
send_field.grid(row=4, column=0, columnspan=2)

name = ''


def send():
    msg = name + " : " + send_field.get()
    encoded_msg = msg.encode()
    encrypted_msg = f.encrypt(encoded_msg)
    s.send(encrypted_msg)
    send_field.delete(0, 'end')


send_button = Button(win, text="send", command=send, background="#2f2f60", foreground="#ffffff", font=14)
send_button.grid(row=4, column=2)


def connect():
    s.connect((ip_field.get(), int(port_field.get())))
    global name
    name = name_field.get()
    confirm = s.recv(1024).decode()
    text_box.config(state="normal")
    text_box.insert('end', confirm + '\n')
    ip_field.config(state="disabled")
    port_field.config(state="disabled")
    name_field.config(state="disabled")
    connect_button.config(state="disabled")
    text_box.config(state="disabled")

    def receive():
        while True:
            msg = s.recv(1024)
            decrpyted_msg = f.decrypt(msg)
            decoded_msg = decrpyted_msg.decode()
            text_box.config(state="normal")
            text_box.insert('end', decoded_msg + '\n')
            text_box.config(state="disabled")
            text_box.yview('end')
            sleep(1)

    t1 = threading.Thread(target=receive)
    t1.start()


connect_button = Button(win, text="Connect", font=14, command=connect, background="#2f2f60", foreground="#ffffff")
connect_button.grid(row=0, column=3)

win.mainloop()
