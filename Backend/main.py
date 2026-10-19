from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import numpy as np
import pandas as pd
from sqlalchemy import text
from sklearn.cluster import DBSCAN
from database import engine

app = FastAPI(title="GeoLease API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "null",
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)

RAIO_KM = 5
MIN_AMOSTRAS = 2
RAIO_TERRA_KM = 6371.0088


@app.get("/")
def inicio():
    return {
        "mensagem": "GeoLease API funcionando!",
        "status": "OK"
    }


@app.get("/imoveis")
def listar_imoveis():
    consulta = text("""
        SELECT
            id,
            nome,
            parque,
            area_ha,
            ST_Y(geom) AS latitude,
            ST_X(geom) AS longitude
        FROM public.imoveis
        WHERE geom IS NOT NULL
        ORDER BY id;
    """)

    with engine.connect() as conexao:
        df = pd.read_sql(consulta, conexao)

    return {
        "total": len(df),
        "imoveis": df.to_dict(orient="records")
    }


@app.get("/dbscan")
def executar_dbscan():
    consulta = text("""
        SELECT
            id,
            nome,
            parque,
            area_ha,
            ST_Y(geom) AS latitude,
            ST_X(geom) AS longitude
        FROM public.imoveis
        WHERE geom IS NOT NULL
        ORDER BY id;
    """)

    with engine.connect() as conexao:
        df = pd.read_sql(consulta, conexao)

    if df.empty:
        return {
            "mensagem": "Nenhum imóvel com coordenadas foi encontrado.",
            "total_imoveis": 0,
            "total_grupos": 0,
            "total_ruidos": 0,
            "imoveis": []
        }

    coordenadas = np.radians(
        df[["latitude", "longitude"]].to_numpy()
    )

    modelo = DBSCAN(
        eps=RAIO_KM / RAIO_TERRA_KM,
        min_samples=MIN_AMOSTRAS,
        metric="haversine"
    )

    df["grupo"] = modelo.fit_predict(coordenadas)

    df["classificacao"] = df["grupo"].apply(
        lambda grupo: "Ruído" if grupo == -1 else f"Grupo {grupo}"
    )

    total_grupos = int(df.loc[df["grupo"] != -1, "grupo"].nunique())
    total_ruidos = int((df["grupo"] == -1).sum())

    return {
        "parametros": {
            "raio_km": RAIO_KM,
            "min_amostras": MIN_AMOSTRAS,
            "metrica": "haversine"
        },
        "total_imoveis": len(df),
        "total_grupos": total_grupos,
        "total_ruidos": total_ruidos,
        "imoveis": df.to_dict(orient="records")
    }
