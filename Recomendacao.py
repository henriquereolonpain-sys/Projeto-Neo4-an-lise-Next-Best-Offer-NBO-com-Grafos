#%%
from neo4j import GraphDatabase
import pandas as pd

URI = "Boa"
USER = "Tentativa"
PASSWORD = "Amigo"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def obter_recomendacoes_hibridas(id_cooperado):
    query = """
    MATCH (alvo:Cooperado {id_cooperado: $id_alvo})
    MATCH (alvo)-[:CONTRATOU]->(:Produto)<-[:CONTRATOU]-(vizinho:Cooperado)
    WHERE vizinho.segmento = alvo.segmento
      AND vizinho.renda_mensal >= alvo.renda_mensal * 0.8
      AND vizinho.renda_mensal <= alvo.renda_mensal * 1.2
    MATCH (vizinho)-[:CONTRATOU]->(recomendacao:Produto)
    WHERE NOT (alvo)-[:CONTRATOU]->(recomendacao)
    RETURN alvo.id_cooperado AS ID_Cooperado,
           recomendacao.nome AS Produto, 
           count(*) AS Score
    ORDER BY Score DESC
    LIMIT 3
    """
    
    with driver.session() as session:
        resultado = session.run(query, id_alvo=id_cooperado)
        registros = [record.data() for record in resultado]
        
    return pd.DataFrame(registros)

df_recomendacoes = obter_recomendacoes_hibridas(1337)
print(df_recomendacoes)

driver.close()
# %%
