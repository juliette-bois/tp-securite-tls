import socket
import threading
import ssl

nickname = input("Choose your nickname: ")

server_host = 'www.binome37.fr'
server_port = 60000

# hostname = 'www.binome37.fr'
# port = 60002

# use TLS Protocol
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# Validate server certificate
context.load_verify_locations('./ca.crt')

# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
client = context.wrap_socket(sock, server_hostname=server_host)
client.connect((server_host, server_port))


def receive():
    while True:  # making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:  # case on wrong ip/port details
            print("An error occured!")
            client.close()
            break


def write():
    while True:  # message layout
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)  # receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)  # sending messages
write_thread.start()
