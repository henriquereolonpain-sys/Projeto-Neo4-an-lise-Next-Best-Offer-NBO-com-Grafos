#%%
from neo4j import GraphDatabase
import pandas as pd

URI = "será"
USER = "que"
PASSWORD = "chove?"

df_cooperados = pd.read_csv('cooperados.csv')
df_interacoes = pd.read_csv('interacoes.csv')

df_contratou = df_interacoes[df_interacoes['tipo_interacao'] == 'CONTRATOU']
df_pesquisou = df_interacoes[df_interacoes['tipo_interacao'] == 'PESQUISOU']

cooperados_dict = df_cooperados.to_dict('records')
contratou_dict = df_contratou.to_dict('records')
pesquisou_dict = df_pesquisou.to_dict('records')

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def carregar_dados(tx):
    tx.run("""
    UNWIND $cooperados AS c
    MERGE (coop:Cooperado {id_cooperado: c.id_cooperado})
    SET coop.idade = c.idade,
        coop.renda_mensal = c.renda_mensal,
        coop.segmento = c.segmento,
        coop.tempo_meses = c.tempo_cooperativa_meses
    """, cooperados=cooperados_dict)

    tx.run("""
    UNWIND $contratos AS i
    MERGE (coop:Cooperado {id_cooperado: i.id_cooperado})
    MERGE (prod:Produto {nome: i.produto})
    MERGE (coop)-[r:CONTRATOU]->(prod)
    SET r.data = i.data
    """, contratos=contratou_dict)

    tx.run("""
    UNWIND $pesquisas AS i
    MERGE (coop:Cooperado {id_cooperado: i.id_cooperado})
    MERGE (prod:Produto {nome: i.produto})
    MERGE (coop)-[r:PESQUISOU]->(prod)
    SET r.data = i.data
    """, pesquisas=pesquisou_dict)

with driver.session() as session:
    print("Iniciando o carregamento")
    session.execute_write(carregar_dados)
    print("Dados carregados com sucesso no Neo4j!")

driver.close()
# %%
