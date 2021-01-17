import hashlib
import json

import requests
from elasticsearch import Elasticsearch, helpers
from flask import Flask, request
from tinydb import TinyDB, Query
from datetime import datetime

from tinydb.operations import add

app = Flask(__name__)

# Ligacao ao TinyDB
dbUsers = TinyDB('DataBase/users', sort_keys=True, indent=4)  # Guarda as informações das máquinas
dbData = TinyDB('DataBase/data', sort_keys=True, indent=4)  # Guarda os dados das máquinas

elastic = Elasticsearch()


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

    # variável para verifcar se esta key já está na base de dados
    exists = dbData.search((Query()['Key'] == req_data['Key']))

    if exists:
        # Se já existir dados para aquela key vamos dar append dos novos valores
        print("A acrescentar os novos valores aos dados antigos da máquina...")
        dbData.update(add('Information', req_data['Information']), (Query()['Key'] == req_data['Key']))
    else:
        # Se a key não existir então vamos adiciona-la e aos valores
        print("A adicionar valores e na base de dados...")
        dbData.insert(req_data)

    print("Valores adicionados")
    treatData()
    return {"status": str(200), "message": "Dados recebidos e guardados com sucesso."}


# Manda os dados para o kibana
def treatData():
    # Vamos buscar todos os dados para mandar para o Kibana
    dataDB = dbData.all()
    # Este array vai guardar em cada posição um conjunto de dados de um utilizador
    # (ex: {Key:X,data:y Values:1},{Key:X,data:h Values:2})
    data_list = []
    # Percorre-se a lista dos dados das maquinas
    for machine in dataDB:
        # Guarda-se a key da maquina
        key = machine['Key']
        # Percorre-se a lista de Dados recolhidos daquela máquina e adiciona-se à lista juntamente com a key e a data
        # para enviar para o Elastic
        for data in machine['Information']:
            data_list.append({'Key': key, 'Date': data['Date'], 'Values': data['Values']})

    # Envia-se para o Elastic
    try:
        print("\nAttempting to index the list of docs using helpers.bulk()")
        # use the helpers library's Bulk API to index list of Elasticsearch docs
        resp = helpers.bulk(
            elastic,
            data_list,
            index="asiindex"
        )
        # print da resposta retornada pelo Elasticsearch
        print("helpers.bulk() RESPONSE:", resp)
        print("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))
    except Exception as err:
        # print any errors returned w
        # Prerequisiteshile making the helpers.bulk() API call
        print("Elasticsearch helpers.bulk() ERROR:", err)
        quit()


# GEra uma vez para criar o index e não corre mais
def genKibana():
    HEADERS = {
        'Content-Type': 'application/json'
    }

    uri = "http://localhost:9200/.kibana/_doc/index-pattern:tempindex"

    query = json.dumps({
        "type": "index-pattern",
        "index-pattern": {
            "title": "asiindex",
            "timeFieldName": "sendTime"
        }
    })

    requests.put(uri, headers=HEADERS, data=query).json()


if __name__ == '__main__':
    app.run()
