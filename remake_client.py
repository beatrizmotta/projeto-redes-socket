import socket 
import threading
from googletrans import LANGUAGES, Translator

HOST = 'localhost'
PORT = 5050

translator = Translator()

print("Choose a language:")
for i in LANGUAGES:
    print(f'- {LANGUAGES[i]} [{i}]')
print("Choose a language: \nExample: 'en', 'pt', 'es'")
language_choosen = input("> ")

nickname_prompt = translator.translate("Qual é o seu apelido?", src='pt', dest=language_choosen).text
room_closed_warning = translator.translate("A sala do chat foi encerrada.", src='pt', dest=language_choosen).text
me_prompt = translator.translate("eu, você nossos", src='pt', dest=language_choosen).text.split(",")[0]

nickname = input(nickname_prompt)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(f'nick={nickname}\lang={language_choosen}'.encode())

def receive():
    while True:
        try:
            data = client.recv(1024).decode()
            language = data.split("\\")[0].split("=")[1]
            msg = data.split("\\")[1].split("=")[1]

            translated_msg = translator.translate(msg, src=language, dest=language_choosen).text
            print(translated_msg)
        except:
            print(room_closed_warning)
            client.close()
            break
        
def send():
    while True:
        msg = input(f'{me_prompt}:')
        client.send(f'{nickname}: {msg}'.encode())

receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()
