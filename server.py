#Hecho conjunto a Lorenzo que ha hecho la clase cliente
import socket
from threading import Thread
from datetime import datetime

#Hecho por María de los Dolores Adamuz Barranco

class Listener(Thread):
    '''Hilo que implementa un canal de comunicación con uno de los clientes
    conectados al servidor de la sala de chat'''

    DATA_SIZE = 1024    # 1 kilobyte para recibir datos
    def __init__(self, sock, chat_server, client_addres):
        super(Listener, self).__init__()
        self.sock = sock
        self.chat_server = chat_server
        self.client_addres=client_addres
        self.dateTime ="["+datetime.now().strftime('%Y-%m-%d || %H:%M')+"]"

    def run(self):
        try:
            while True:
                client_data=self.sock.recv(self.DATA_SIZE)
                self.chat_server.broadcast(client_data, self.sock)
        except:
            print(str(self.client_addres)+": ...se ha desconectado")
            self.sock.close()

class ChatServer:
    '''Servidor de una sala de chat'''

    def __init__(self, address, port, max_users):
        self.address = address
        self.port = port
        self.max_users = max_users  # Límite de usuarios
        self.sock = socket.socket()
        self.client_socks = set()  # Saca los clientes conectados (conjunto)

    def setup_sock(self):
        '''Inicializa el socket creado en el constructor'''
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, int(self.port)))
        self.sock.listen(self.max_users)

    def broadcast(self, msg, chatServer):
        '''Difunde el mensaje recibido a todos los usuarios conectados'''
        for i in self.client_socks:
            if i != chatServer:
                i.send(msg)
 

    def run(self):
        '''Arranca el servicio y acepta conexiones de clientes indeipidamente'''
        self.setup_sock()
        print("Servidor en funcionamiento y esperando conexiones")
        try:
            while True:
                if len(self.client_socks) >= self.max_users:
                    dato="la sala se encuentra llena espera un momento"
                    actual.send(dato.encode())
                    actual.close()
                else:
                    actual, ip = self.sock.accept()
                    self.client_socks.add(actual)
                    print("["+datetime.now().strftime('%Y-%m-%d || %H:%M')+"]: "+str(ip)+":acaba de unirse al chat ")
                    salachat =Listener(actual, self, ip)
                    salachat.start()
        except:
            actual.close()
            self.sock.close()

if __name__ == '__main__':       #Esto es que lo puse asi porque en mi pc en 127.0.0.1 y el 5555 para probar las cosas más rápido
    address = input("ingrese la dirección ip del servidor: ")

    if(address==""):
        adress = "127.0.0.1"
    port = input("Ingrese el puerto de conexión: ")
    if(port ==""):
        port ="55555"
    max_users = 10
    server = ChatServer(address, port, max_users)
    server.run()