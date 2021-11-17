import socket
import ssl
import threading

hostname = 'www.binome37.fr'
port = 60000

clients = []
nicknames = []

# use TLS Protocol
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# use server certificate and public key
context.load_cert_chain('./ca_server.crt', './rsa_server_key.pem', password='coucou')

# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind((hostname, port))
sock.listen()

# wrap socket with context
server = context.wrap_socket(sock, server_side=True)


def broadcast(message):  # broadcast function declaration
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:  # receiving valid messages from client
            message = client.recv(1024)
            broadcast(message)
        except:  # removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():  # accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
