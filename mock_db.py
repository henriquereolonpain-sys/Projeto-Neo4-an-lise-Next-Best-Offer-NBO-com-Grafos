#%% 
import pandas as pd 
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

n_cooperados = 5000

segmentos = ['Agro', 'PF', 'PJ']
probs_segmentos = [0.20, 0.63, 0.17]

ids_cooperados = np.arange(1, n_cooperados + 1)
idades = np.random.randint(18, 75, n_cooperados)
rendas = np.random.lognormal(mean=8.5, sigma=0.8, size=n_cooperados).round(2)
segmento_atribuido = np.random.choice(segmentos, n_cooperados, p=probs_segmentos)
tempo_meses = np.random.randint(1, 120, n_cooperados)

df_cooperados = pd.DataFrame({
    'id_cooperado': ids_cooperados,
    'idade': idades,
    'renda_mensal': rendas,
    'segmento': segmento_atribuido,
    'tempo_cooperativa_meses': tempo_meses
})

produtos = {
    'Agro': ['Custeio Agricola', 'Seguro Safra', 'Consorcio Trator', 'CPR'],
    'PF': ['Cartao Black', 'Emprestimo Pessoal', 'Seguro de Vida', 'Consorcio Carro', 'Previdencia'],
    'PJ': ['Antecipacao de Recebiveis', 'Giro Caixa', 'Maquininha', 'Seguro Empresarial']
}

interacoes = []
tipos_interacao = ['CONTRATOU', 'PESQUISOU']
probs_interacao = [0.6, 0.4]

for index, row in df_cooperados.iterrows():
    seg = row['segmento']
    produtos_possiveis = produtos[seg]
    
    qtd_interacoes = np.random.randint(1, 6)
    
    produtos_escolhidos = random.choices(produtos_possiveis, k=qtd_interacoes)
    
    for prod in produtos_escolhidos:
        tipo = np.random.choice(tipos_interacao, p=probs_interacao)
        dias_atras = np.random.randint(1, 365)
        data_interacao = datetime.now() - timedelta(days=dias_atras)
        
        interacoes.append({
            'id_cooperado': row['id_cooperado'],
            'produto': prod,
            'tipo_interacao': tipo,
            'data': data_interacao.strftime('%Y-%m-%d')
        })

df_interacoes = pd.DataFrame(interacoes)

df_cooperados.to_csv('cooperados.csv', index=False)
df_interacoes.to_csv('interacoes.csv', index=False)

# %%
