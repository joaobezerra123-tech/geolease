from sqlalchemy import text
from database import engine

print("Banco configurado:", engine.url.database)
print("Servidor configurado:", engine.url.host)

try:
    with engine.connect() as conexao:
        banco = conexao.execute(
            text("SELECT current_database()")
        ).scalar_one()

        postgis = conexao.execute(
            text("SELECT PostGIS_Full_Version()")
        ).scalar_one()

        print("Conexao realizada com sucesso!")
        print(f"Banco conectado: {banco}")
        print(f"PostGIS: {postgis}")

except Exception as erro:
    print("Nao foi possivel conectar ao banco.")
    print(erro)