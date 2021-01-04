import psutil


def getAllPorts():
    """Retorna as conexões de todos os sockets da máquina"""
    return psutil.net_connections(kind=all)

# Fazer para portas especificas!
