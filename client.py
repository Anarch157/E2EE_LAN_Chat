import socket
from time import sleep
from threading import *

print("Enter server local ip address")
ip = input()
print("Enter server local port number")
port = int(input())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

print(s.recv(1024).decode("ascii"))

class Receiver(Thread):
    def run(self):
        while True:
            recvd_msg = s.recv(1024)
            print(recvd_msg.decode("ascii"))
            sleep(1)

class Sender(Thread):
    def run(self):
        while True:
            sent_msg = input()
            s.send(bytes(sent_msg, "ascii"))
            sleep(1)

rec = Receiver()
sen = Sender()

rec.start()
sleep(0.5)
sen.start()
