import socket
from time import sleep
from threading import *

print("Enter your local ip address")
ip = input()
print("Enter your local port number")
port = int(input())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
s.listen(1)

c, addr = s.accept()
print(f"[+] Connection from {addr} has been established")
c.send(bytes("[+] Connected to the server", "ascii"))


class Receiver(Thread):
    def run(self):
        while True:
            recvd_msg = c.recv(1024)
            print(recvd_msg.decode("ascii"))
            sleep(1)


class Sender(Thread):
    def run(self):
        while True:
            sent_msg = input()
            c.send(bytes(sent_msg, "ascii"))
            sleep(1)


rec = Receiver()
sen = Sender()

rec.start()
sleep(0.5)
sen.start()
