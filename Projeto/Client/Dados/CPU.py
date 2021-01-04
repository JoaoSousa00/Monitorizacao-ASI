import psutil


def getNumberCPUs():
    """Retorna o número de CPUs na máquina"""
    return psutil.cpu_count(logical=False)


def getPercentageUsageCPU(file_loc):
    """Retorna a percentagem média de uso dos CPUs na máquina"""
    return psutil.cpu_percent(interval=1)


def getPercentageUsagePerCPU():
    """Retorna a percentagem de uso por CPU da máquina"""
    return psutil.cpu_percent(interval=1, percpu=True)
