import os
import platform

import psutil


def getDiskInfo():
    """Retorna a informação do disco"""
    # Onde se vai guardar a informação dos discos
    data = []

    # all=False para apenas retornar discos fisicos (por exemplo: hard disks, cd-rom drives, USB keys)
    partitions = psutil.disk_partitions(all=False)

    for partition in partitions:
        try:
            # Dados de uma partição
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk = {"Mountpoint": partition.mountpoint, "DiskTotal": partition_usage.total,
                    "DiskUsage": partition_usage.used, "DiskFree": partition_usage.free,
                    "DiskPercent ": partition_usage.percent}
        except PermissionError:
            print("Erro ao acessar as particoes do disco.")
            continue

        if platform.system() == "Linux":
            # Se for Linux vai também buscar os dados dos inodes
            inodes = os.statvfs(partition.mountpoint)

            # Calcula-se a percentagem fazendo a divisao dos inodes free pelo total de inodes e multiplicando por 100
            percentage_inodes = (float(inodes.f_ffree) / inodes.f_files) * 100

            disk.update({"InodesPercent": percentage_inodes})

    # Guardar os dados de cada partição
    data.append(disk)

    return data
