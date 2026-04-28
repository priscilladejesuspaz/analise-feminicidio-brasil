import pandas as pd
import numpy as np

df = pd.read_csv('../data/raw/feminicidio_serie_historica.csv')

print(df.head())
print('Qtd:', df.shape)
print(df.isnull().sum())

print(df['SEXO'].value_counts())

df = df[['DT_NASCIMENTO', 'DT_OBITO', 'SEXO', 'TIPO_OBITO', 'CAUSA_BASICA', 'COD_MUNICIPIO_OBITO']].copy()

df['DT_NASCIMENTO'] = df['DT_NASCIMENTO'].astype(str).str.replace('.0', '', regex=False).str.zfill(8)
df['DT_OBITO'] = df['DT_OBITO'].astype(str).str.replace('.0', '', regex=False).str.zfill(8)

df['DT_NASCIMENTO'] = pd.to_datetime(df['DT_NASCIMENTO'], format='%d%m%Y', errors='coerce')
df['DT_OBITO'] = pd.to_datetime(df['DT_OBITO'], format='%d%m%Y', errors='coerce')

print(df[['DT_NASCIMENTO', 'DT_OBITO']].head(10))

df = df.dropna(subset=['DT_NASCIMENTO', 'DT_OBITO']).dropna(axis=1)

print(df.shape)

print(df['DT_NASCIMENTO'].isna().sum())
print(df.shape)

df['IDADE'] = (df['DT_OBITO'] - df['DT_NASCIMENTO']).dt.days / 365
#df = df['DT_NASCIMENTO'].fillna(df['DT_NASCIMENTO'].mean())

df = df[(df['IDADE'] > 10) & (df['IDADE'] < 90)]

print(df['IDADE'].describe())
print(df.shape)

print(df.columns)

print("MÉDIA:", df['IDADE'].mean())
print(df['IDADE'].min())
print(df['IDADE'].max())

print(df.shape)