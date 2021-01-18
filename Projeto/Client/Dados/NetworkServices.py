import socket

import psutil


def getAllPorts():
    """Retorna as conexões de todos os sockets da máquina"""
    return psutil.net_connections(kind=all)


def isPortActive(port):
    """
    Método que avalia se uma porta está aberta ou fechada.

    Returns: True, se a porta estiver aberta ou, False, se estiver fechada
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()

    if result == 0:
        return True
    else:
        return False
