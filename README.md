# produto-python — API FastAPI + MySQL no Railway

API de teste com a tabela `produto (id, descricao, preco)`.

## Rodar localmente
```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env         # e preencha com os dados do MySQL
uvicorn app:app --reload       # http://localhost:8000/docs
python teste_api.py
```

## Deploy no Railway
1. Suba esta pasta para um repositório no GitHub (o `.env` NÃO vai, está no `.gitignore`).
2. No projeto do Railway (onde já está o MySQL): **+ Create > GitHub Repo** > escolha o repositório.
3. No serviço da aplicação > **Variables > Raw Editor**, cole:
```
MYSQLHOST=${{MySQL.MYSQLHOST}}
MYSQLPORT=${{MySQL.MYSQLPORT}}
MYSQLUSER=${{MySQL.MYSQLUSER}}
MYSQLPASSWORD=${{MySQL.MYSQLPASSWORD}}
MYSQLDATABASE=${{MySQL.MYSQLDATABASE}}
```
4. Clique em **Deploy** e acompanhe os logs até ficar **Active**.
5. **Settings > Networking > Generate Domain** e acesse `https://SEU-DOMINIO/docs`.

| Método | Rota | Corpo |
|---|---|---|
| GET | /produtos | – |
| GET | /produtos/{id} | – |
| POST | /produtos | `{"descricao": "...", "preco": 10.5}` |
| PUT | /produtos/{id} | `{"descricao": "...", "preco": 10.5}` |
| DELETE | /produtos/{id} | – |
