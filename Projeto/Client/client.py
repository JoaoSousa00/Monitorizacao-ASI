import psutil
import requests

total = dict(psutil.virtual_memory()._asdict())['total']
free = dict(psutil.virtual_memory()._asdict())['available']

data = {"total": total, "free": free}

# Enviar os dados para o servidor usando o WebService
res = requests.post('http://localhost:5000/setData', json=data)

if res.ok:
    print(res.json())
