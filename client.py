# Comando de execução do programa pelo terminal: py client.py

import socket # Biblioteca padrão.
import threading # Biblioteca padrão.
from googletrans import LANGUAGES, Translator # pip install googletrans==4.0.0-rc1

# Definindo endereço IP e de porta do servidor.
HOST = 'localhost'
PORT = 5050

# Checagem para input do idioma escolhido pelo usuário.
def language_validator(language_code):
    while language_code not in LANGUAGES.keys():
        print("Language code not valid, please type another:")
        language_code = input("> ")
    return language_code 

translator = Translator()

# Exibe os idiomas disponíveis ao usuário.
print("Choose a language:")
for i in LANGUAGES:
    print(f'- {LANGUAGES[i]} [{i}]')

# Input do idioma.
print("Choose a language: \nExample: 'en', 'pt', 'es'")
language_choosen = input("> ")
language_choosen = language_validator(language_choosen)

# Input do nome do usuário.
nickname_prompt = translator.translate("Qual é o seu apelido?", src='pt', dest=language_choosen).text
# Tradução da mensagem exibida quando o servidor é encerrado.
room_closed_warning = translator.translate("A sala do chat foi encerrada.", src='pt', dest=language_choosen).text

nickname = input(nickname_prompt + ' ')

# Criando socket no formato IPv4 (INET - requisita host e port) e com conexão TCP (STREAM).
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectando cliente ao servidor na porta "PORT".
client.connect((HOST, PORT))
# Envia ao servidor as informações do usuário.
client.send(f'nick={nickname}\lang={language_choosen}'.encode())

is_server_up = True

# Função de recepção dos dados.
def receive():
    while True:
        try:
            # Recebe e decodifica os dados transmitidos pelo servidor com no máximo 1024 bits.
            data = client.recv(1024).decode()
            # Tratamento dos dados.
            language = data.split("\\")[0].split("=")[1]
            msg = data.split("\\")[1].split("=")[1]
            # Traduz a mensagem recebida para o idioma do usuário.
            translated_msg = translator.translate(msg, src=language, dest=language_choosen).text
            print(translated_msg)

        except:
            # Exceção para quando o servidor é encerrado.
            print(room_closed_warning)
            client.close()
            global is_server_up
            is_server_up = False
            break
    return 

# Função de envio dos dados para o servidor.       
def send():
    while True:
        msg = input()
        
        if (is_server_up):
            client.send(f'{nickname}: {msg}'.encode())
        else:
            break

# Cria uma thread de recepção e envio.
receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)
# Inicialização da thread.
receive_thread.start()
send_thread.start()
