import psutil

# Verificar se funciona para Linux
def getDiskInfo():
    """Retorna a informação do disco"""
    # Onde se vai guardar a informação dos discos
    data = []

    # all=False para apenas retornar discos fisicos (por exemplo: hard disks, cd-rom drives, USB keys)
    partitions = psutil.disk_partitions(all=False)

    for partition in partitions:
        try:
            # Dados de uma particção
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            print("Erro ao acessar as particoes do disco.")
            continue

    # Guardar os dados de cada partição
    data.append({"Mountpoint": partition.mountpoint, "DiskTotal": partition_usage.total,
                 "DiskUsage": partition_usage.used, "DiskFree": partition_usage.free,
                 "DiskPercent ": partition_usage.percent})

    return data
