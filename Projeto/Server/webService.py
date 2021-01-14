import hashlib

from flask import Flask, request
from tinydb import TinyDB
from datetime import datetime

app = Flask(__name__)

# Ligacao ao TinyDB
dbData = TinyDB('DataBase/data', sort_keys=True, indent=4, separators=(',', ': '))  # Guarda os dados das máquinas


@app.route('/configuration', methods=['POST'])  # GET requests will be blocked
def genKey():
    req_data = request.get_json()

    # Informações da máquina que fez o pedido
    ip = req_data['ip']
    so = req_data['so']

    # cria uma string que vai ser posteriormente codificada. Esta string contem a data atual e ip e so recebidos
    secret = str(datetime.now()) + ip + so

    # A key é feita usando sha512
    key = hashlib.sha512(secret.encode()).hexdigest()

    # Guarda-se os dados da máquina na Base de Dados
    dbData.insert({"key": key, "IP": ip, "SO": so})  # # # COMO GUARDAR???

    # Find ALL
    print(dbData.all())

    return {"status": str(201), "key": key}


@app.route('/setData', methods=['POST'])  # GET requests will be blocked
def setData():
    req_data = request.get_json()

    ip = req_data['ip']
    so = req_data['so']

    ins = {}
    ins['token'] = "memory"
    ins["data"] = req_data
    ins["valores"] = datetime.now()
    ins["expressoes"] = {"value": ip}
    json_body = [ins]

    dbData.insert({"ip": ip})

    # Find ALL
    print(dbData.all())

    return {"status": str(200)}


if __name__ == '__main__':
    app.run()
