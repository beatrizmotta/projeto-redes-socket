import socket
import logging
import threading 
from googletrans import Translator
#####     SCRIPT DE CHAT     #####
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
clients = dict()

should_work = True

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
            print("Estou teoricamente fechando")
            global should_work
            should_work = False

            for client in clients:
                clients[client]["connection"].close()

            server.shutdown(socket.SHUT_RDWR)
            server.close()
            break
    return 

def transmitir(msg, address_code):
    decoded_msg = msg.decode()
    nickname_transmissor = decoded_msg.split(":")[0]
    language = clients[address_code]["language"]

    for client in clients:
        if (clients[client]['nick'] != nickname_transmissor):
            clients[client]['connection'].send(f'lang={language}\\msg={decoded_msg}'.encode())

def handle_client(client, address_code):
    while True:
        print("Handling client")
        # Handle Client vai tentar receber algo do outro lado do socket.
        # Caso ele consiga, ele faz o decode da mensagem recebida e lida com ela,
        # fazendo o 'cadastro' do emissor caso seja a primeira vez que ele estabelece
        # o contato com o servidor (a primeira mensagem enviada pelo cliente
        # sempre vai conter apenas o seu nome de usuário e linguagem) ou transmitindo
        # a mensagem mandada caso contrário. 
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
        
        # Caso não consiga receber a mensagem (ocorreu algum erro na função recv) então
        # a conexão com tal client deve ser fechada e ele deve ser retirado da lista de 
        # usuários ativos. 
        except: 
            alias = clients[address_code]['nick']
            clients[address_code]['connection'].close()
            del clients[address_code]
            transmitir(f"{alias} saiu do chat", address_code)
            break
    return 
        

def main():
    
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

main()