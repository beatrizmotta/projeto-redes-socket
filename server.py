# Comando de execução do programa pelo terminal: py server.py

import socket # Biblioteca padrão.
import logging # Biblioteca padrão.
import threading # Biblioteca padrão.
from googletrans import Translator # pip install googletrans==4.0.0-rc1

#####     SCRIPT DE CHAT     #####
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
clients = dict()

# Definindo endereço IP e de porta do servidor.
HOST = 'localhost'
PORT = 5050 
# Criando socket no formato IPv4 (INET - requisita host e port) e com conexão TCP (STREAM).
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Servidor visível apenas dentro do dispositivo nos endereços de HOST e PORT.
server.bind((HOST, PORT))

translator = Translator()

# Inicialização do modo de escuta do servidor.
server.listen() 
logging.info("Servidor rodando")

# Função de controle para encerrar o servidor.
def control():
    while True:
        control = input(">> ")
        if (control == '/quit'):
            server.close()

# Função de transmissão para todos os clientes conectados ao servidor (envio da mensagem, nome e idioma do remetente).
def transmitir(msg, address_code):
    decoded_msg = msg.decode()
    nickname_transmissor = decoded_msg.split(":")[0]
    language = clients[address_code]["language"]

    for client in clients:
        if (clients[client]['nick'] != nickname_transmissor):
            clients[client]['connection'].send(f'lang={language}\\msg={decoded_msg}'.encode())

# Função de recepção dos dados com no máximo 1024 bytes.
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
        # Exceção para quando um cliente se desconecta do servidor.
        except:
            alias = clients[address_code]['nick']
            clients[address_code]['connection'].close()
            del clients[address_code]
            for client1 in clients:
                clients[client1]['connection'].send(f"lang=pt\\msg={alias} saiu da sala".encode())
            break
        
# Criação e inicialização da thread de controle.
control_thread = threading.Thread(target=control)
control_thread.start()

while True:
    # Recebe os dados do cliente, quando o servidor aceita a conexão.
    client, address = server.accept()
    logging.info(f'{address} was connected')

    address = "".join([str(i) for i in list(address)])

    # Adiciona o novo cliente ao dict() com seu respectivo endereço IP.
    clients[address] = {
        'connection': client,
        'nick': ''
    }

    # Criação e inicialização da thread de controle de clientes.
    thread = threading.Thread(target=handle_client, args=(client, address))
    thread.start()
    
