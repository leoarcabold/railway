"""
API simples de produtos (id, descricao, preco) - FastAPI + MySQL
Mesma arquitetura do exemplo Spring Boot: GitHub -> Railway (App + MySQL)
Documentação interativa automática em /docs (Swagger)
"""
import os
from contextlib import asynccontextmanager

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

# Localmente lê o arquivo .env; no Railway as variáveis vêm do painel "Variables"
load_dotenv()


# ----------------------------- BANCO -----------------------------

def conectar():
    """Abre conexão usando as MESMAS variáveis que o Railway gera para o MySQL."""
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", "localhost"),
        port=int(os.getenv("MYSQLPORT", "3306")),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQLPASSWORD", ""),
        database=os.getenv("MYSQLDATABASE", "railway"),
    )


def executar(sql, params=None, buscar=None):
    """Executa um comando SQL. buscar = 'um', 'todos' ou None (insert/update/delete)."""
    con = conectar()
    try:
        cur = con.cursor(dictionary=True)
        cur.execute(sql, params or ())
        if buscar == "um":
            resultado = cur.fetchone()
        elif buscar == "todos":
            resultado = cur.fetchall()
        else:
            con.commit()
            resultado = {"linhas": cur.rowcount, "id": cur.lastrowid}
        cur.close()
        return resultado
    finally:
        con.close()


def criar_tabela():
    """Equivalente ao ddl-auto=update do JPA: cria a tabela se não existir."""
    executar("""
        CREATE TABLE IF NOT EXISTS produto (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descricao VARCHAR(100) NOT NULL,
            preco DECIMAL(10,2) NOT NULL
        )
    """)


# ----------------------------- MODELOS -----------------------------
# Pydantic valida os dados de entrada (papel parecido com DTO + @Valid no Spring)

class ProdutoEntrada(BaseModel):
    descricao: str = Field(min_length=1, max_length=100, examples=["Mouse sem fio"])
    preco: float = Field(ge=0, examples=[79.90])


class Produto(ProdutoEntrada):
    id: int


# ----------------------------- APLICAÇÃO -----------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executa ao iniciar a aplicação (local e no Railway)
    try:
        criar_tabela()
    except Exception as e:
        print(f"[AVISO] Não foi possível criar/verificar a tabela: {e}")
    yield


app = FastAPI(
    title="API de Produtos",
    description="Exemplo de deploy FastAPI + MySQL no Railway",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["status"])
def inicio():
    return {"status": "API de produtos no ar", "docs": "/docs", "rota": "/produtos"}


@app.get("/produtos", response_model=list[Produto], tags=["produtos"])
def listar():
    return executar("SELECT * FROM produto ORDER BY id", buscar="todos")


@app.get("/produtos/{id}", response_model=Produto, tags=["produtos"])
def buscar(id: int):
    produto = executar("SELECT * FROM produto WHERE id = %s", (id,), buscar="um")
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@app.post("/produtos", response_model=Produto, status_code=201, tags=["produtos"])
def inserir(dados: ProdutoEntrada):
    r = executar("INSERT INTO produto (descricao, preco) VALUES (%s, %s)",
                 (dados.descricao, dados.preco))
    return Produto(id=r["id"], **dados.model_dump())


@app.put("/produtos/{id}", response_model=Produto, tags=["produtos"])
def atualizar(id: int, dados: ProdutoEntrada):
    # Confere se existe (o MySQL retorna 0 linhas afetadas se os valores forem iguais)
    if not executar("SELECT id FROM produto WHERE id = %s", (id,), buscar="um"):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    executar("UPDATE produto SET descricao = %s, preco = %s WHERE id = %s",
             (dados.descricao, dados.preco, id))
    return Produto(id=id, **dados.model_dump())


@app.delete("/produtos/{id}", status_code=204, tags=["produtos"])
def excluir(id: int):
    r = executar("DELETE FROM produto WHERE id = %s", (id,))
    if r["linhas"] == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
