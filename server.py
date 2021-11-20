import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9090))
s.listen(5)

clients = []


def broadcast(message):
    for client in clients:
        client.send(message)


def interact(client):
    while True:
        try:
            msg = client.recv(1024)
            print(msg.decode())
            broadcast(msg)

        except:
            clients.remove(client)
            client.close()
            break


def connect():
    while True:
        client, address = s.accept()
        print(f"[+] Someone connected with {address}")
        clients.append(client)
        client.send("[+] Connected to the server".encode())

        t1 = threading.Thread(target=interact, args=(client,))
        t1.start()


connect()
