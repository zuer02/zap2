
import threading
import socket
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

backend = default_backend()

block_size = 16 # tamanho do bloco da de msg, tem de ser multiplo de 16

PORT = 7777
SERVER_IP = 'localhost'

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((SERVER_IP, PORT))
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')

    username = input('Nome do usuário: ')
    print('\n',username,' conectado a ',SERVER_IP,' na porta ',PORT,'!\n')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


def receiveMessages(client): # os print eu usei para debug
    while True:
        try:
            msg_rcvd = client.recv(2048)
            # print(f'encrypted msg received: {msg_rcvd}')
            
            key = msg_rcvd[:32]
            received_iv = msg_rcvd[32:48]
            print(f'received iv: {received_iv}')
            msg_to_decrypt = msg_rcvd[48:]
            print(f'msg to decrypt: {msg_to_decrypt}')

            aes = algorithms.AES(key)
            cbc = modes.CBC(received_iv)
            cipherDC = Cipher(aes, cbc, backend=backend)
            decryptor = cipherDC.decryptor() # decriptador
            unpadder = padding.PKCS7(128).unpadder()
            
            dec_ct = decryptor.update(msg_to_decrypt) + decryptor.finalize()
            print(f'msg after decryption: {dec_ct}')

            msg_unpad = unpadder.update(dec_ct)
            print(f'unpadded msg: {msg_unpad}')            
            
            print(msg_unpad.decode('utf-8', errors='ignore'))
        except Exception as e:
            print('\nNão foi possível permanecer conectado no servidor! Erro: ',e,'\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            

def sendMessages(client, username):
    while True:
        try:
            # cipher object for encryption
            key = os.urandom(32)
            iv = os.urandom(16) # vetor de inicialização
            print(f' send iv: {iv}')

            aes = algorithms.AES(key)
            cbc = modes.CBC(iv)
            cipherEN = Cipher(aes, cbc, backend=backend)
            encryptor = cipherEN.encryptor() # encriptador
            padder = padding.PKCS7(128).padder()

            msg = input('\n')
            msg = f'{username}: {msg}' # para ir o username e a msg
            b_msg = bytearray(msg, encoding="ascii")
            n = len(b_msg)
            spaces_add = block_size - n % block_size
            new_b_msg = bytearray(msg + ' ' * spaces_add, encoding="utf8")
            padder = padding.PKCS7(128).padder()
            msg_pad = padder.update(new_b_msg) + padder.finalize()
            print(f'padded msg: {msg_pad}')
            ct = encryptor.update(msg_pad) + encryptor.finalize() # envia o iv mais a msg encrypted
            msg_send = key + iv + ct
            try: 
                print(f'msg after + key + iv & encryption: {msg_send}')
                client.send(msg_send)
            except Exception as e:
                print('error: ', e)
                
        except:
            return

main()


