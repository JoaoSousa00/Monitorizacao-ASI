from flask import Flask, request
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)

# Ligacao ao TinyDB
dbUsers = TinyDB('DataBase/users')  # Guarda os utilizadores e os seus dados
dbData = TinyDB('DataBase/data')  # Guarda os dados das máquinas dos utilizadores


@app.route('/setData', methods=['POST'])  # GET requests will be blocked
def setData():

    req_data = request.get_json()

    total_mem = req_data['total']
    free_mem = req_data['free']

    ins = {}
    ins['measurement'] = "memory"
    ins["tags"] = req_data
    ins["time"] = datetime.now()
    ins["fields"] = {"value": total_mem}
    json_body = [ins]

    dbData.insert({"ola": "aqui"})

    # Find ALL
    print(dbData.all())

    return {"status": str(200)}


if __name__ == '__main__':
    app.run()
