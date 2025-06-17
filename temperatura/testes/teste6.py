import os
import pandas as pd


municipios_data = "municipios.xls"
df_ibge = pd.read_excel(municipios_data, skiprows=6)
print(df_ibge['Região Geográfica Imediata'].nunique())

df2 = pd.read_csv('temperatura/dengue/DENGBR23.csv', low_memory=False, usecols= ['ID_MUNICIP'], dtype={"ID_MUNICIP": "int64"})
qtd_municipios = df2["ID_MUNICIP"].nunique()
# Converte para string e calcula o comprimento
df2["ID_MUNICIP_STR"] = df2["ID_MUNICIP"].astype(str)

# Ver o número de caracteres de cada código
df2["LENGTH"] = df2["ID_MUNICIP_STR"].str.len()

# Frequência dos comprimentos
print(df2["LENGTH"].value_counts().sort_index())