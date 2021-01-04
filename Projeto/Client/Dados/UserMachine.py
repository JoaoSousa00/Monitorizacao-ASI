from socket import socket


def getIP():
    ip = socket.gethostbyname(socket.gethostname())
