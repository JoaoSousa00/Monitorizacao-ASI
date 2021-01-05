import psutil
import requests
from Client.Dados import Memory

total = Memory.getTotalMemory()
free = Memory.getFreeMemory()

data = {"total": total, "free": free}

# Enviar os dados para o servidor usando o WebService
res = requests.post('http://localhost:5000/setData', json=data)

if res.ok:
    print(res.json())
