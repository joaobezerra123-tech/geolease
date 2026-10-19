
import pandas as pd
from sqlalchemy import text
from sklearn.cluster import DBSCAN
from database import engine

RAIO_KM = 5
MIN_AMOSTRAS = 2
RAIO_TERRA_KM = 6371.0088

consulta = text("""
    SELECT
        id,
        nome,
        parque,
        ST_Y(geom) AS latitude,
        ST_X(geom) AS longitude
    FROM public.imoveis
    WHERE geom IS NOT NULL
    ORDER BY id;
""")

with engine.connect() as conexao:
    df = pd.read_sql(consulta, conexao)

if df.empty:
    print("Nenhum imóvel com coordenadas foi encontrado.")
else:
    coordenadas = df[["latitude", "longitude"]].values
    coordenadas_rad = __import__("numpy").radians(coordenadas)

    modelo = DBSCAN(
        eps=RAIO_KM / RAIO_TERRA_KM,
        min_samples=MIN_AMOSTRAS,
        metric="haversine"
    )

    df["grupo"] = modelo.fit_predict(coordenadas_rad)

    for _, imovel in df.iterrows():
        grupo = imovel["grupo"]
        classificacao = "Ruído" if grupo == -1 else f"Grupo {grupo}"

        print(
            f"ID: {imovel['id']} | "
            f"Nome: {imovel['nome']} | "
            f"Parque: {imovel['parque']} | "
            f"Classificação: {classificacao}"
        )

    print("\nQuantidade de grupos encontrados:",
          df.loc[df["grupo"] != -1, "grupo"].nunique())

    print("Quantidade de imóveis classificados como ruído:",
          (df["grupo"] == -1).sum())
