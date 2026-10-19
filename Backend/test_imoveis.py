
from sqlalchemy import text
from database import engine

consulta = text("""
    SELECT
        i.id,
        i.nome,
        i.parque,
        i.area_ha,
        ST_Y(i.geom) AS latitude,
        ST_X(i.geom) AS longitude
    FROM public.imoveis AS i
    WHERE i.geom IS NOT NULL
    ORDER BY i.id;
""")

with engine.connect() as conexao:
    resultado = conexao.execute(consulta)

    for imovel in resultado:
        print(
            f"ID: {imovel.id} | "
            f"Nome: {imovel.nome} | "
            f"Parque: {imovel.parque} | "
            f"Área: {imovel.area_ha} ha | "
            f"Latitude: {imovel.latitude} | "
            f"Longitude: {imovel.longitude}"
        )
