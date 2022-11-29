import socket
import logging
import threading 
from googletrans import Translator

#####     SCRIPT DE CHAT     #####
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
clients = dict()

HOST = 'localhost'
PORT = 5050 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
translator = Translator()

server.listen() 
logging.info("Servidor rodando")

def control():
    while True:
        control = input(">> ")
        if (control == '/quit'):
            server.close()

def transmitir(msg, address_code):
    decoded_msg = msg.decode()
    nickname_transmissor = decoded_msg.split(":")[0]
    language = clients[address_code]["language"]

    for client in clients:
        if (clients[client]['nick'] != nickname_transmissor):
            clients[client]['connection'].send(f'lang={language}\\msg={decoded_msg}'.encode())

def handle_client(client, address_code):
    while True:
        try:
            data = client.recv(1024)
            decoded_data = data.decode()
            print(decoded_data)
            if (decoded_data.startswith("nick=")):
                client_info = decoded_data.split("\\")
                nickname = client_info[0].split("=")[1]
                language = client_info[1].split("=")[1]
                clients[address_code]['nick'] = nickname
                clients[address_code]['language'] = language  
            else:
                transmitir(data, address_code)

        except:
            alias = clients[address_code]['nick']
            clients[address_code]['connection'].close()
            del clients[address_code]
            for client1 in clients:
                clients[client1]['connection'].send(f"lang=pt\\msg={alias} saiu da sala".encode())
            break
        

control_thread = threading.Thread(target=control)
control_thread.start()

while True:
    
    client, address = server.accept()
    logging.info(f'{address} was connected')

    print(type(address))
    address = "".join([str(i) for i in list(address)])

    clients[address] = {
        'connection': client,
        'nick': ''
    }

    thread = threading.Thread(target=handle_client, args=(client, address))
    thread.start()
    