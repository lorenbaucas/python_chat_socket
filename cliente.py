# Cliente del ejercicio conjunto para la práctica de PSP, hecho con María de los Dolores Adamuz Barranco (servidor)

#Hecho por Lorenzo Bautista Castellano

import socket
from threading import Thread
from datetime import datetime


class Listener(Thread):
    '''Hilo que implementa un canal de comunicación entre el servidor
    que proporciona el servicio de una sala de chat y el cliente actual'''
    DATA_SIZE = 1024    # 1 kilobyte para recibir datos

    def __init__(self, sock):
        super(Listener, self).__init__()
        self.sock = sock
        self.dateTime="["+datetime.now().strftime('%Y-%m-%d || %H:%M')+"]"

    def run(self):
        try:
            while True:
                data=self.sock.recv(self.DATA_SIZE)
                print(self.dateTime+": "+data.decode())
        except:
            self.sock.close()
            exit()


class ChatClient:
    '''Cliente para el servidor de una sala de chat'''

    def __init__(self, address, port, nickname):
        self.address = address
        self.port = port
        self.nickname = " ("+nickname+") dice: "
        self.sock = socket.socket()

    def setup_sock(self):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       #para realizar la conexión con el servidor
        try:
            self.sock.connect((self.address, int(self.port)))
        except:
            self.sock.close()

    def run(self):
        self.setup_sock()
        print("Ahora puedes comenzar a escribir")
        try:
            while True:
                l=Listener(self.sock)
                l.start()
                my_data=self.nickname+input()
                self.sock.send(my_data.encode())
        except:
            print("Se ha producido un error")
            self.sock.close()

if __name__ == '__main__':
    address = input("Ingrese la dirección IP del servidor: ")
    if(address==""): #lo puso asi para ir probando más rapido
       adress = "127.0.0.1"
    port = input("Ingrese el puerto de conexión: ")
    if(port ==""):
        port ="55555"
    nickname = input("Introduzca su nombre de usuario: ")
    client = ChatClient(address, port, nickname)
    client.run()