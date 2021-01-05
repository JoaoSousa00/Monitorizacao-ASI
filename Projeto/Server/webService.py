import os

from flask import Flask, request
from tinydb import TinyDB, Query
from datetime import datetime

from Server.Logs import LogsTreatment

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

    dbData.insert({"total": total_mem})

    os.system('python3 Logs/apache-fake-log-gen.py -n 100 -o LOG -p Logs/StoredLogs/')

    print(LogsTreatment.getLogsInfo("Logs/StoredLogs"))
    # Find ALL
    print(dbData.all())

    return {"status": str(200)}


if __name__ == '__main__':
    app.run()
