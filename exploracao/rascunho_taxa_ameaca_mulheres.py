import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max.columns', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('../data/raw/taxa_ameaca_vitimas_mulheres.csv', sep=';', encoding='cp1252')

print(df.head().to_string())

print('QTD', df.shape)

print(df.dtypes)

print("==='\nValores nulos\n===")
print(df.isnull().sum())
df = df.dropna(subset=['Estado', 'Ano', 'Valor'])
df = df.drop(columns = ['Tipo Valor', 'Indicador', 'Categoria', 'Localidade'], errors='ignore')
print(df.head().to_string())

print(df.isnull().sum())

print(df.head().to_string())

df.columns = df.columns.str.lower()

print(df.describe().to_string())
# Verificando se a coluna tem algum Valor antes de apagar
print(df.nunique())
# Convertendo o Valor de String para Float
df['valor'] = df['valor'].str.replace(',', '.').astype(float)

print(df['valor'].head())
print(df['valor'].dtype)

df.to_csv('taxa_ameaca_vit_mulheres_tratada.csv', index=False, sep=';',encoding='latin-1')

print(df.columns)

import sys
print(sys.stdout.encoding)