import pandas as pd
import matplotlib.pyplot as plt
import os

pasta = 'temperatura/dadosAgrupados'
pasta_graficos = 'temperatura/graficos'

# Criar pasta para salvar gráficos se não existir
os.makedirs(pasta_graficos, exist_ok=True)

# Listar todos os arquivos CSV na pasta
arquivos = [f for f in os.listdir(pasta) if f.endswith('.csv')]

for arquivo in arquivos:
    caminho = os.path.join(pasta, arquivo)
    
    try:
        df = pd.read_csv(caminho, skiprows=2)
        df['DATA'] = pd.to_datetime(df['DATA'])
        df['semana'] = df['DATA'].dt.isocalendar().week
        casos_por_semana = df.groupby('semana')['casos'].sum()

        plt.figure(figsize=(10,6))
        casos_por_semana.plot(kind='bar')
        plt.title(f'Casos por semana em 2024 - {arquivo}')
        plt.xlabel('Semana do ano')
        plt.ylabel('Número de casos')

        nome_png = os.path.join(pasta_graficos, f'grafico_{arquivo.replace(".csv", "")}.png')
        plt.savefig(nome_png)
        plt.close()

        print(f'Gráfico salvo: {nome_png}')
    
    except Exception as e:
        print(f'Erro ao processar {arquivo}: {e}')
