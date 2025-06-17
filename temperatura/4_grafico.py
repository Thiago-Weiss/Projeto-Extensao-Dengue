import pandas as pd
import matplotlib.pyplot as plt
import os

# Caminhos
arquivo_mapeamento = "temperatura/dadosTratados/temperatura/__index_processado.csv"  # ← arquivo com ARQUIVO,CODIGO_MUNICIPIO,etc
pasta_parquet = "temperatura/dadosTratados/temperatura"          # ← onde estão os arquivos .parquet
codigo_alvo = 421660                                   # ← código da cidade desejada (ex: São José)

# Carregar o mapeamento
df_mapa = pd.read_csv(arquivo_mapeamento)

# Verificar se o código existe
linha = df_mapa[df_mapa["CODIGO_MUNICIPIO"] == codigo_alvo]

if linha.empty:
    print(f"❌ Código {codigo_alvo} não encontrado no arquivo de mapeamento.")
else:
    nome_arquivo = linha.iloc[0]["ARQUIVO"]
    caminho_arquivo = os.path.join(pasta_parquet, nome_arquivo)

    if not os.path.exists(caminho_arquivo):
        print(f"❌ Arquivo '{nome_arquivo}' não encontrado em '{pasta_parquet}'.")
    else:
        print(f"✅ Carregando dados de: {nome_arquivo}")

        # Ler o .parquet
        df = pd.read_parquet(caminho_arquivo)
        df.to_csv("regiaoTemperatura.csv", index= False)

        # Converter DATA para datetime se necessário
        if not pd.api.types.is_datetime64_any_dtype(df["DATA"]):
            df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")

        # Checar colunas esperadas
        colunas = [
            "DATA", 
            "CHUVA", 
            "TEMP MAX GRAUS", 
            "TEMP MIN GRAUS", 
            "UMID MAX PORCENTAGEM", 
            "UMID MIN PORCENTAGEM"
        ]
        if not all(col in df.columns for col in colunas):
            print("❌ O arquivo não contém todas as colunas esperadas.")
        else:
            # Gráfico 1 - Temperatura
            plt.figure(figsize=(15, 5))
            plt.plot(df["DATA"], df["TEMP MAX GRAUS"], label="Temp Máx (°C)", color="red")
            plt.plot(df["DATA"], df["TEMP MIN GRAUS"], label="Temp Mín (°C)", color="orange")
            plt.title("Temperatura Máxima e Mínima - São José (2024)")
            plt.xlabel("Data")
            plt.ylabel("Temperatura (°C)")
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.legend()
            plt.tight_layout()
            plt.show()

            # Gráfico 2 - Umidade
            plt.figure(figsize=(15, 5))
            plt.plot(df["DATA"], df["UMID MAX PORCENTAGEM"], label="Umidade Máx (%)", color="blue")
            plt.plot(df["DATA"], df["UMID MIN PORCENTAGEM"], label="Umidade Mín (%)", color="green")
            plt.title("Umidade Máxima e Mínima - São José (2024)")
            plt.xlabel("Data")
            plt.ylabel("Umidade (%)")
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.legend()
            plt.tight_layout()
            plt.show()

            # Gráfico 3 - Chuva
            plt.figure(figsize=(15, 5))
            plt.bar(df["DATA"], df["CHUVA"], label="Chuva (mm)", color="blue", width=1)
            plt.title("Chuva Diária - São José (2024)")
            plt.xlabel("Data")
            plt.ylabel("Chuva (mm)")
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.show()
