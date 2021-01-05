import os
import time

import requests
from Client.Dados import UserMachine
from Client.Logs import LogsTreatment


def askToken():

    ip = UserMachine.getIP()

    so = UserMachine.getSO()

    data = {"ip": ip, "so": so}

    os.system('python3 Logs/apache-fake-log-gen.py -n 100 -o LOG -p Logs/StoredLogs/')

    print(LogsTreatment.getLogsInfo("Logs/StoredLogs"))

    # Enviar os dados para o servidor usando o WebService
    res = requests.post('http://localhost:5000/setData', json=data)

    if res.ok:
        print(res.json())


while True:
    askToken()
    time.sleep(300) # Adormece o cliente por 5 minutos e depois manda mais dados
