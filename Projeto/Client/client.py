from datetime import datetime
import os
import time

import requests
from Client.Dados import CPU, Disk, Memory, NetworkServices, UserMachine
from Client.Logs import LogsTreatment
from os import path


def askKey():
    # Vai mandar um pedido ao servidor para que este o guarde e retorne uma key que nos identificará

    print("A verificar se já está registado...")

    # ip da máquina
    ip = UserMachine.getIP()

    # sistema operativo da máquina
    so = UserMachine.getSO()

    data = {"ip": ip, "so": so}

    # Enviar os dados da máquina para o servidor usando o WebService
    res = requests.post('http://localhost:5000/configuration', json=data)

    if res.json()['status'] == "409":
        # Se a resposta for 409 então a máquina já existe
        print("Bem vindo de volta.")
    else:
        print("Registo bem sucedido")

    # Guardar a key
    token = res.json()['key']

    # Verifica se o ficheiro existe
    if not path.exists("key.txt"):
        # Se existir apenas vamos buscar o token do utilizador e vamos mandar os dados ao servidor com esse
        # identificador

        f = open("key.txt", "w")
        f.write(token)
        f.close()

    sendData(key=token)


def sendData(key):
    print("A recolher informação do sistema...")

    # Data de começo das monitorizações
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Memória
    memoryData = {"Total": Memory.getTotalMemory(), "InUse": Memory.getUsedMemory(), "Free": Memory.getFreeMemory()}

    # CPU
    cpuData = {"Number": CPU.getNumberCPUs(), "Percentage": CPU.getPercentageUsageCPU()}

    # Disco
    diskData = Disk.getDiskInfo()

    # Portas, uso como exemplo a porta 1024 normalmente usada pelo windows e a porta 8080 normalmente inutilizada
    portsData = {"1024": NetworkServices.isPortActive(1024), "8080": NetworkServices.isPortActive(8080)}

    # Gerar logs
    os.system('python3 Logs/apache-fake-log-gen.py -n 10 -o LOG -p Logs/StoredLogs/')

    logsData = LogsTreatment.getLogsInfo("Logs/StoredLogs")
    print(logsData)
    print("Informação recolhida\nA preparar envio dos dados...")

    # Aqui junta-se todos os dados da monitorização em formato json
    monitData = {"Memory": memoryData, "CPU": cpuData, "Disk": diskData, "Ports": portsData, "Logs": logsData}

    # Agora junta-se a key com os dados da monitorização num json para se poder mandar para o servidor
    generalData = {"Key": key, "Values": [{date: monitData}]}

    res = requests.post('http://localhost:5000/setData', json=generalData)

    if res.ok:
        print("Dados enviados com sucesso")
    else:
        print("O envio de dados não teve sucesso")


def run():
    while True:
        askKey()
        time.sleep(300)  # Adormece o cliente por 5 minutos e depois manda mais dados


run()
