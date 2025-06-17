import pandas as pd
import time

# Arquivo CSV
caminho_csv = 'temperatura/dengue/DENGBR24.csv'
caminho_parquet = 'temperatura/dengue/DENGBR24_limpo.parquet'

# Mede o tempo para ler parquet
start_read = time.time()
df_parquet = pd.read_parquet(caminho_parquet)
end_read = time.time()
print(f"Tempo para ler parquet: {end_read - start_read:.5f} segundos")

# Opcional: mostrar algumas linhas para verificar
print(df_parquet.info())
