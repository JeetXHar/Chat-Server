from socket import *
import threading

IP='localhost'
PORT=8020

server=socket(AF_INET,SOCK_STREAM)
server.bind((IP,PORT))
print("Server Running at: ",IP,PORT)

server.listen()
print("Server listing...")

clients={}
socket_list=[]

def handle(client):
    while True:
        try:
            message=(clients[client]+'> '+client.recv(1024).decode('ascii')).encode('ascii')
            
            for c in clients:
                if c != client:
                    c.send(message)
        except:
            print('Closed connection from:',clients[client])
            for c in clients:
                if c!=client:
                    c.send((clients[client]+' left the chat').encode('ascii'))
            del clients[client]
            socket_list.remove(client)
            client.close()
            break
def receive():
    while True:
        try:
            client, addr = server.accept()
            username=client.recv(1024).decode('ascii')

            print('New connection:',*addr,':',username)
            for c in clients:
                c.send((username+' joined the chat').encode('ascii'))
            socket_list.append(client)
            clients[client]=username

            threat = threading.Thread(target=handle,args=(client,))
            threat.start()
        except:
            print("Server Closing")
            exit()

receive()



