import platform
import socket


def getIP():
    """Retorna o IP da Máquina"""
    return socket.gethostbyname(socket.gethostname())


def getSO():
    """Retorna o Sistema Operativo da Máquina"""
    return platform.system()
