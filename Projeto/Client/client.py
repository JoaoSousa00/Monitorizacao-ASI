import os
import time

import requests
from Client.Dados import UserMachine
from Client.Logs import LogsTreatment
from os import path


def askToken():
    # Verifica se o ficheiro existe
    if(path.exists("key.txt")):
        # Se existir apenas vamos buscar o token do utilizador e vamos mandar os dados ao servidor com esse
        # identificador

        f = open("key.txt", "r")
        token = f.readline()
        f.close()
    else:
        # Se não existir vai mandar um pedido ao servidor para que este o guarde e retorne uma key que nos identificará

        # ip da máquina
        ip = UserMachine.getIP()

        # sistema operativo da máquina
        so = UserMachine.getSO()

        data = {"ip": ip, "so": so}

        print(data)  # TIRARRRRRRRRRRR

        # Enviar os dados da máquina para o servidor usando o WebService
        res = requests.post('http://localhost:5000/setData', json=data)

        if res.ok:
            print(res.json())
            token = res.json()["key"]

            f = open("key.txt", "w")
            f.write(token)
            f.close()

            ### Mandar dados
        else:
            # Se a resposta não for ok então não mandamos os dados
            return

    # Gerar logs
    os.system('python3 Logs/apache-fake-log-gen.py -n 10 -o LOG -p Logs/StoredLogs/')

    # Calcular as expressões do log
    print(LogsTreatment.getLogsInfo("Logs/StoredLogs"))  # TIRARRRRRRRRRRR


while True:
    askToken()
    time.sleep(300)  # Adormece o cliente por 5 minutos e depois manda mais dados
