import socket 
import threading
from googletrans import LANGUAGES, Translator

HOST = 'localhost'
PORT = 5050

def language_validator(language_code):
    while language_code not in LANGUAGES.keys():
        print("Language code not valid, please type another:")
        language_code = input("> ")
    return language_code 

translator = Translator()

print("Choose a language:")
for i in LANGUAGES:
    print(f'- {LANGUAGES[i]} [{i}]')

print("Choose a language: \nExample: 'en', 'pt', 'es'")
language_choosen = input("> ")
language_choosen = language_validator(language_choosen)

nickname_prompt = translator.translate("Qual é o seu apelido?", src='pt', dest=language_choosen).text
room_closed_warning = translator.translate("A sala do chat foi encerrada.", src='pt', dest=language_choosen).text
# me_prompt = translator.translate("eu, você nossos", src='pt', dest=language_choosen).text.split(",")[0]

nickname = input(nickname_prompt + ' ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(f'nick={nickname}\lang={language_choosen}'.encode())

is_server_up = True

def receive():
    while True:
        try:
            data = client.recv(1024).decode()
            language = data.split("\\")[0].split("=")[1]
            msg = data.split("\\")[1].split("=")[1]

            translated_msg = translator.translate(msg, src=language, dest=language_choosen).text
            # print ("\033[A                             \033[A")
            print(translated_msg)

        except Exception as e:
            #print(e)
            print(room_closed_warning)
            client.close()
            global is_server_up
            is_server_up = False
            break
    # print("RECEIVE -- reached the end of the loop")
    return 
        
def send():
    while True:
        msg = input()
        
        if (is_server_up):
            client.send(f'{nickname}: {msg}'.encode())
        else:
            break


receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()
