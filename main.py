import logging

from fastapi import FastAPI, HTTPException, Path, Query, Request, Response
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError

from database import executar_sql

app = FastAPI(title="API REST 2INFO3")

@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("unicorn.error").error("Erro de BD: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro em acesso ao BD"},
    )

def representar_produtos(produto):
    return {
        "id": produto["id"],
        "nome": produto["nome"],
        "categoria": produto["categoria"],
        "preco": format(produto["preco"], ".2f"),
    }

@app.get("/produtos")
def listar_produtos():
    sql = "SELECT * FROM produtos"
    produtos = executar_sql(sql)
    return {
        "dados": [representar_produtos(produto) for produto in produtos],
        "instrucaosql": {"sql": sql, "parametros": []} 
    }