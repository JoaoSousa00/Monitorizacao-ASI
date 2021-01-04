import psutil


def getTotalMemory():
    """Retorna a memória total da máquina"""
    return dict(psutil.virtual_memory()._asdict())['total']


def getFreeMemory():
    """Retorna a memória livre da máquina"""
    return dict(psutil.virtual_memory()._asdict())['available']


def getUsedMemory():
    """Retorna a memória usada da máquina"""
    return dict(psutil.virtual_memory()._asdict())['used']
