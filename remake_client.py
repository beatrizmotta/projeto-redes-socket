import socket 
import threading
from googletrans import LANGUAGES, Translator

def language_validator(language_code):
    while language_code not in LANGUAGES.keys():
        print("Language code not valid, please type another:")
        language_code = input("> ")
    return language_code 

HOST = 'localhost'
PORT = 5050

translator = Translator()

print("Choose a language:")
for i in LANGUAGES:
    print(f'- {LANGUAGES[i]} [{i}]')
print("Choose a language: \nExample: 'en', 'pt', 'es'")
language_choosen = input("> ")
language_choosen = language_validator(language_choosen)

nickname_prompt = translator.translate("Qual é o seu apelido?", src='pt', dest=language_choosen).text
room_closed_warning = translator.translate("A sala do chat foi encerrada.", src='pt', dest=language_choosen).text
me_prompt = translator.translate("eu, você nossos", src='pt', dest=language_choosen).text.split(",")[0]

room_open = True



nickname = input(nickname_prompt)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(f'nick={nickname}\lang={language_choosen}'.encode())

def receive():
    while True:
        try:
            # A Receive vai tentar receber algo do outro lado do código. 
            # Caso ele consiga, ele vai separar a mensagem em mensagem e linguagem.
            #
            data = client.recv(1024).decode()
            language = data.split("\\")[0].split("=")[1]
            msg = data.split("\\")[1].split("=")[1]

            translated_msg = translator.translate(msg, src=language, dest=language_choosen).text
            print(translated_msg)
        except:
            # Caso não consiga receber, ele deve fechar a conexão também
            print(room_closed_warning)
            room_open = False
            client.close()
            break
    return
        
def send():
    while True:
        if not room_open:
            print("Eita fechou")
            break
        msg = input(f'{me_prompt}:')
        client.send(f'{nickname}: {msg}'.encode())
    return

receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()
