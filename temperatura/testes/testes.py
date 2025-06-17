import pandas as pd
import os

# Caminhos
clima_index = pd.read_csv("temperatura/processados/index_final.csv")  # tem: ARQUIVO, ID_MUNICIPIO
df_dengue = pd.read_csv("temperatura/dengue/DENGBR24.csv", low_memory=False)  # tem: DATA, ID_MUNICIPIO, CASOS

# Garante que a data é datetime
df_dengue["DATA"] = pd.to_datetime(df_dengue["DT_NOTIFIC"])

# Diretório onde estão os CSVs de clima
dir_clima = "temperatura/processados"
dir_saida = "temperatura/saida_completa"
os.makedirs(dir_saida, exist_ok=True)


print(df_dengue["ID_MUNICIP"].unique()[:50])

# Converte a coluna para string e remove espaços em branco
df_dengue["ID_MUNICIP"] = df_dengue["ID_MUNICIP"].astype(str).str.strip()

# Define o lugar que quer buscar também como string e sem espaços
lugar = "120020".strip()

# Agora faz o filtro
df_dengue_mun = df_dengue[df_dengue["ID_MUNICIP"] == lugar]

print(df_dengue_mun)

# lugar = "120020"
# df_dengue_mun = df_dengue[df_dengue["ID_MUNICIP"] == lugar]
# print(df_dengue_mun)

# lugar = "120010"
# df_dengue_mun = df_dengue[df_dengue["ID_MUNICIP"] == lugar]
# print(df_dengue_mun)

# lugar = "520870"
# df_dengue_mun = df_dengue[df_dengue["ID_MUNICIP"] == lugar]
# print(df_dengue_mun)

# lugar = "520006"
# df_dengue_mun = df_dengue[df_dengue["ID_MUNICIP"] == lugar]
# print(df_dengue_mun)


for _, linha in clima_index.iterrows():
    break
    nome_arquivo = linha["ARQUIVO"]
    id_municipio = linha["ID_MUNICIP"]

    # Caminho completo do CSV de clima
    caminho_clima = os.path.join(dir_clima, nome_arquivo)

    # Lê o CSV do clima
    df_clima = pd.read_csv(caminho_clima)
    df_clima["DATA"] = pd.to_datetime(df_clima["DATA"])

    # Filtra os casos de dengue desse município
    df_dengue_mun = df_dengue[df_dengue["ID_MUNICIP"] == id_municipio]


    # Filtra dengue por município
    df_dengue_mun = df_dengue[df_dengue["ID_MUNICIP"] == id_municipio]

    # Conta casos por data
    casos_por_data = df_dengue_mun.groupby("DATA").size().rename("CASOS").reset_index()

    # Junta ao clima por DATA
    df_resultado = pd.merge(df_clima, casos_por_data, on="DATA", how="left")

    # Preenche dias sem casos com 0
    df_resultado["CASOS"] = df_resultado["CASOS"].fillna(0).astype(int)

    # Salva novo arquivo
    saida_arquivo = os.path.join(saida, nome_arquivo)
    df_resultado.to_csv(saida_arquivo, index=False)
    print(f"[OK] Processado: {nome_arquivo}")

    # # Junta os dados pela data
    # df_final = pd.merge(df_clima, df_dengue_mun[["DATA", "CASOS"]], on="DATA", how="left")

    # # Renomeia a coluna se quiser
    # df_final.rename(columns={"CASOS": "CASOS_DENGUE"}, inplace=True)

    # # Salva novo CSV
    # df_final.to_csv(os.path.join(dir_saida, nome_arquivo), index=False)
