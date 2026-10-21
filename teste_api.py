"""Testa a API. Troque BASE pela URL gerada no Railway (Settings > Networking)."""
import requests

BASE = "http://localhost:8000"   # ex.: "https://seu-app-production.up.railway.app"

print("POST:", requests.post(f"{BASE}/produtos",
      json={"descricao": "Pen Drive 64GB", "preco": 59.90}).json())

produtos = requests.get(f"{BASE}/produtos").json()
print("GET lista:", produtos)

ultimo = produtos[-1]["id"]
print("PUT:", requests.put(f"{BASE}/produtos/{ultimo}",
      json={"descricao": "Pen Drive 64GB USB 3.0", "preco": 64.90}).json())
print("GET um:", requests.get(f"{BASE}/produtos/{ultimo}").json())
print("DELETE status:", requests.delete(f"{BASE}/produtos/{ultimo}").status_code)
