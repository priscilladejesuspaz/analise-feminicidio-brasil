import pandas as pd 

pd.set_option('display.width', None)
pd.set_option('display.max.columns', None)
pd.set_option('display.max_colwidth', None)

# Lendo o arquivo de Raça / Instrução (Tratando o erro de parser)
df = pd.read_csv('../data/raw/raca_nivel_instrucao.csv',
                 sep= (';'),
                 encoding='utf-8', 
                 engine='python', # Utiliza quando o pandas não reconhece o separador, este comando força para o modelo python
                 skiprows=5, # Pula os cabeçalhos do csv, caso contenha dados sujos
                 header=None)

print(f"A minha tabela tem {len(df.columns)} colunas.")
# 2. Achatando as colunas para facilitar a manipulação
# Isso vai criar nomes como "2016_Branca"
# print(df.head)
# print(df.columns)

# Criamos uma lista com os nomes na ordem exata das colunas

novas_columns = [
    'estado', 'instrucao',          # 1, 2
    'total_2016', 'branca_2016', 'preta_parda_2016', # 3, 4, 5
    'total_2017', 'branca_2017', 'preta_parda_2017', # 6, 7, 8
    'total_2018', 'branca_2018', 'preta_parda_2018', # 9, 10, 11
    'total_2019', 'branca_2019', 'preta_parda_2019', # 12, 13, 14
    'total_2022', 'branca_2022', 'preta_parda_2022', # 15, 16, 17
    'total_2023', 'branca_2023', 'preta_parda_2023'  # 18, 19, 20
]

# Agora sim!
df.columns = novas_columns
print("Sucesso! Colunas renomeadas.")

# Visualizar os dados 
print(df.head())

# Remove as linhas que não têm dados reais (notas de rodapé)
df = df.dropna(subset=['total_2016'])

# Remove a coluna "Brasil", deixando somente os estados 
df = df[df['estado'] != 'Brasil']

# Limpa espaços extras (ex: " Acre" vira "Acre")
df['estado'] = df['estado'].str.strip()
df['instrucao'] = df['instrucao'].str.strip()

# Mostra apenas as 3 primeiras colunas para ver se o nome bate com o dado
print(df[['estado', 'instrucao', 'total_2016']].head(10))

# O 'id_vars' são as colunas que NÃO queremos mexer (que identificam a linha)
# O 'var_name' é o nome da nova coluna que guardará os nomes antigos (ex: total_2016)
# O 'value_name' é o nome da coluna que guardará os números (a população)
df_longo = df.melt(
    id_vars=['estado', 'instrucao'],
    var_name='categoria_ano',
    value_name='populacao'
)
print(df_longo.head(15))

# Fatiamento de texto: 
# 1. Pegamos apenas os últimos 4 caracteres da coluna (o ano)
df_longo['ano'] = df_longo['categoria_ano'].str[-4:]

# 2. Pegamos tudo o que vem ANTES do ano (a raça / categoria)
# Removemos o '_' e o ano do final 
df_longo['raca_cor'] = df_longo['categoria_ano'].str[:-5]

# 3. Convertemos o ano para número para bater com o outro arquivo
df_longo['ano'] = pd.to_numeric(df_longo['ano'])

print(df_longo.head())

# df_final = pd.merge(df_feminicio, df_longo = on=['estado', 'ano'])

# ORGANIZAÇÃO DA MESA: Coloca os dados em ordem alfabética de estado e ordem cronológica. 
# Isso serve para que, ao abrir o arquivo no SQL ou Looker, os dados de um mesmo 
# estado fiquem todos "juntinhos" e fáceis de conferir, em vez de espalhados.

df_longo = df_longo.sort_values(by=['estado', 'ano', 'raca_cor', 'instrucao'])

# =========================
# CALCULAR PERCENTUAL NEGRO
# =========================

# FILTRAR TOTAL
df_longo = df_longo[df_longo['instrucao'] == 'Total']

# PADRONIZAR
df_longo['raca_cor'] = df_longo['raca_cor'].str.strip().str.lower()

# AGRUPAR TOTAL
df_total = df_longo[df_longo['raca_cor'] == 'total'] \
    .groupby(['estado', 'ano'])['populacao'].sum().reset_index()

# AGRUPAR PRETA/PARDA
df_negra = df_longo[df_longo['raca_cor'] == 'preta_parda'] \
    .groupby(['estado', 'ano'])['populacao'].sum().reset_index()

# JUNTAR
df_final = pd.merge(df_total, df_negra, on=['estado', 'ano'])

df_final.columns = ['estado', 'ano', 'pop_total', 'pop_negra']

# CALCULAR %
df_final['perc_negra'] = df_final['pop_negra'] / df_final['pop_total']

# VERIFICAR
print(df_final.head())
print(df_longo['instrucao'].unique())


df_final.to_csv(
    '../data/processed/perc_raca.csv',
    sep=';',
    index=False,
    encoding='utf-8'
)