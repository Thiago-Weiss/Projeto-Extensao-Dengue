import requests
import pandas as pd
import os
import csv
from time import sleep
import unidecode
import PathManager
import LogManager


# colunas do csv
parametro_data = "DT_NOTIFIC"
parametro_codigo_municipio = "ID_MUNICIP"

colunas_necessarias = [
    parametro_data,
    parametro_codigo_municipio,
]


df_dengue = pd.read_csv(
    PathManager.dengue_file,
    parse_dates=[parametro_data],
    usecols=colunas_necessarias,
    dtype={
        parametro_codigo_municipio: "Int64",
    })

df_dengue.dropna(subset=[parametro_codigo_municipio], inplace=True)



# Agrupa por município e data, contando os casos
casos_por_dia = (
    df_dengue
    .groupby([parametro_codigo_municipio, parametro_data])
    .size()
    .reset_index(name='casos')
)


 


parametro_index_codigo_municipio = 'CODIGO_MUNICIPIO'
parametro_arquivo = "ARQUIVO"
parametro_temperatura_data = "DATA"


# Carrega o index.csv
df_index = pd.read_csv(PathManager.indexTemperaturaProcesada_file, dtype={parametro_index_codigo_municipio: 'Int64'})

i = 0
# Itera pelos municípios com dados de casos
for municipio, grupo in casos_por_dia.groupby(parametro_codigo_municipio):

    # Verifica se município está no index.csv
    linha_index = df_index[df_index[parametro_index_codigo_municipio] == municipio]

    if linha_index.empty:
        continue

    nome_arquivo = linha_index[parametro_arquivo].values[0]
    caminho_parquet = os.path.join(PathManager.temperaturaTratadas_dir, nome_arquivo)

    if not os.path.exists(caminho_parquet):
        continue

    # Carrega o parquet com dados diários de temperatura
    df_temperatura = pd.read_parquet(caminho_parquet)
    
    # Garante que a coluna 'DATA' seja datetime
    df_temperatura[parametro_temperatura_data] = pd.to_datetime(df_temperatura[parametro_temperatura_data])

    # Dados de casos para o município
    df_casos_municipio = grupo[[parametro_data, 'casos']].rename(columns={
        parametro_data: parametro_temperatura_data
    })

    # Faz o merge com base na DATA
    df_resultado = pd.merge(df_temperatura, df_casos_municipio, on='DATA', how='left')

    # Preenche casos ausentes com 0
    df_resultado['casos'] = df_resultado['casos'].fillna(0).astype(int)


    # Calcula casos totais no ano para o município

    
    i += 1
    caminho_csv = os.path.join(PathManager.dadosAgrupados_dir, f"dado{i}.csv")

    # Escreve a primeira linha com código do município e casos totais
    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        casos_ano = grupo['casos'].sum()
        chuva_ano = df_resultado['CHUVA'].sum()
        writer = csv.writer(f)
        writer.writerow(['codigo_municipio', 'casos_ano', 'chuva_anual'])
        writer.writerow([municipio, casos_ano, chuva_ano ])

    # Escreve o dataframe a partir da segunda linha, com cabeçalho
    df_resultado.to_csv(caminho_csv, mode='a', index=False, header=True, encoding='utf-8')

    print(i)
    print(df_resultado.head())
    print()
