## Filtra e retorna um subgrafo isolando nós específicos
```MATCH (c:Cooperado)-[r]->(p:Produto)
WHERE c.id_cooperado IN [1, 2, 3]
RETURN c, r, p
```

## Algoritmo de recomendação
```MATCH (alvo:Cooperado {id_cooperado: 1})-[:CONTRATOU]->(:Produto)<-[:CONTRATOU]-(vizinho:Cooperado)
MATCH (vizinho)-[:CONTRATOU]->(recomendacao:Produto)
WHERE NOT (alvo)-[:CONTRATOU]->(recomendacao)
RETURN recomendacao.nome AS Produto_Recomendado, count(*) AS Score_de_Relevancia
ORDER BY Score_de_Relevancia DESC
LIMIT 3
```

## Visualização macro
```MATCH (c:Cooperado)-[r]->(p:Produto)
WITH c, r, p, rand() as aleatorio
ORDER BY aleatorio
LIMIT 5000
RETURN c, r, p
```