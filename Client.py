from socket import *
import threading
import signal

exit_event=threading.Event()

IP='localhost'
PORT=8020

username=input("Enter username: ")

client=socket(AF_INET,SOCK_STREAM)

client.connect((IP,PORT))
client.send(username.encode('ascii'))

def recieve():
    while True:
        if exit_event.is_set(): break
        try:
            message=client.recv(1024).decode('ascii')
            print(message)
        except:
            client.close()
            exit()
            break

def write():
    while True:
        if exit_event.is_set():break
        try:
            message=input()
            client.send(message.encode('ascii'))

        except:
            client.close()
            exit()
            break

def sig_han(signum,frame):
    exit_event.set()

signal.signal(signal.SIGINT,sig_han)

recieve_threat=threading.Thread(target=recieve)
recieve_threat.start()

write_threat=threading.Thread(target=write)
write_threat.start()

recieve_threat.join()
write_threat.join()