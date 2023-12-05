import threading
import socket


clients = []

PORT = 7777
SERVER_IP = 'localhost'

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((SERVER_IP, PORT))
        server.listen()
        print('Servidor ligado em ', SERVER_IP, ' na porta ', PORT)
    except Exception as e:
        return print(f"\nNão foi possível iniciar o servidor! Erro: {e}\n")

    while True:
        client, addr = server.accept()
        clients.append(client)
        print(addr)
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            broadcast(msg, client)
        except:
            clients.remove(client)
            print('Um usuário foi desconectado. Usuários conectados: ', len(clients))
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                clients.remove(client)

main()