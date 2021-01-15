import hashlib

from flask import Flask, request
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)

# Ligacao ao TinyDB
dbData = TinyDB('DataBase/data', sort_keys=True, indent=4)  # Guarda os dados das máquinas
dbUsers = TinyDB('DataBase/users', sort_keys=True, indent=4)  # Guarda as informações das máquinas


@app.route('/configuration', methods=['POST'])  # GET requests will be blocked
def genKey():
    req_data = request.get_json()

    # Informações da máquina que fez o pedido
    ip = req_data['ip']
    so = req_data['so']

    machine = dbUsers.search((Query()['IP'] == ip) & (Query()['SO'] == so))

    if machine:
        # Se a máquina já existe mandamos um aviso e a key da máquina
        return {"status": str(409), "message": "Uma máquina com esse IP e SO já existe.", "key": machine[0]['Key']}

    # Cria uma string que vai ser posteriormente codificada. Esta string contem a data atual, IP e SO recebidos
    secret = str(datetime.now()) + ip + so

    # A key é feita usando sha512
    key = hashlib.sha512(secret.encode()).hexdigest()

    # Guarda-se os dados da máquina na Base de Dados
    dbUsers.insert({"Key": key, "IP": ip, "SO": so})

    return {"status": str(201), "key": key}


@app.route('/setData', methods=['POST'])  # GET requests will be blocked
def setData():
    req_data = request.get_json()

    print(req_data)

    # Ver se já tem a key na BD:
    # -> Se houver vamos dar append dos dados
    # -> Se não houver vamos simplesmente adicionar os dados que vieram

    if True:
        print("ola")
        # Ir buscar o json da key e depois fazer um upsert lá
    else:
        dbData.insert(req_data)

    return {"status": str(200)}


if __name__ == '__main__':
    app.run()
