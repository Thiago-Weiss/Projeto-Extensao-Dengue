import pandas as pd
import matplotlib.pyplot as plt
import PathManager

# Parâmetros
parametro_data = "DT_SIN_PRI"
parametro_codigo_municipio = "ID_MN_RESI"

colunas_necessarias = [
    parametro_data,
    parametro_codigo_municipio,
]

# Leitura do arquivo
df_dengue = pd.read_csv(
    PathManager.dengue_file,
    parse_dates=[parametro_data],
    usecols=colunas_necessarias,
    dtype={parametro_codigo_municipio: "Int64"},
)




# Códigos dos municípios
florianopolis = 420540 
palhoca       = 421190 
saoJose       = 421660
cidades = [florianopolis, palhoca, saoJose]


# Mapear nomes das cidades
mapa_cidades = {
    florianopolis: "Florianópolis",
    palhoca: "Palhoça",
    saoJose: "São José"
}

# Filtrar apenas as 3 cidades
df_cidades = df_dengue[df_dengue[parametro_codigo_municipio].isin(cidades)].copy()

df_cidades["Cidade"] = df_cidades[parametro_codigo_municipio].map(mapa_cidades)

# Filtrar intervalo entre fevereiro e julho (qualquer ano)
df_cidades = df_cidades[
    df_cidades[parametro_data].dt.month.between(2, 6)
]

# Pivotar para ter colunas por cidade
df_agrupado = df_cidades.groupby([parametro_data, "Cidade"]).size().reset_index(name="Casos")
df_pivot = df_agrupado.pivot(index=parametro_data, columns="Cidade", values="Casos").fillna(0)
# Verificação: certifique-se de que há dados
if df_pivot.empty:
    print("⚠️ Nenhum dado disponível entre fevereiro e julho para as cidades selecionadas.")
else:
    # Plotar
    plt.figure(figsize=(14, 6))
    df_pivot.plot(ax=plt.gca(), linewidth=2)

    plt.title("Casos Diários de Dengue por Cidade (Fev–Jun)")
    plt.xlabel("Data")
    plt.ylabel("Número de Casos")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.legend(title="Cidade")

    # Mostrar total de casos por cidade
    totais = df_cidades["Cidade"].value_counts()
    for cidade, total in totais.items():
        print(f"{cidade}: {total} casos entre fevereiro e julho")

    plt.show()



# Supondo que df_cidades contém os dados filtrados entre fevereiro e julho
df_cidades["dia_semana"] = df_cidades[parametro_data].dt.dayofweek  # 0 = segunda, 6 = domingo

# Agrupar por dia da semana
casos_por_dia = df_cidades.groupby("dia_semana").size()

# Mostrar nomes dos dias
dias_nomes = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
casos_por_dia.index = [dias_nomes[d] for d in casos_por_dia.index]

# Plotar
casos_por_dia.plot(kind="bar", color="orange", title="Casos de Dengue por Dia da Semana (Fev–Jul)")
plt.ylabel("Número de Casos")
plt.xlabel("Dia da Semana")
plt.grid(True, axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

# Agrupar por data e contar casos por dia
serie_diaria = df_cidades.groupby(parametro_data).size()

# Plotar autocorrelação
plot_acf(serie_diaria, lags=60)
plt.title("Autocorrelação dos Casos Diários de Dengue (Feb–Jul)")
plt.xlabel("Defasagem (dias)")
plt.ylabel("Correlação")
plt.tight_layout()
plt.show()



import numpy as np
import matplotlib.pyplot as plt

# Supondo que 'serie_diaria' é sua série de casos diários já agrupada por data
y = serie_diaria.values
n = len(y)

# Aplicar FFT
fft = np.fft.fft(y - np.mean(y))  # Remover média para focar nos ciclos
freq = np.fft.fftfreq(n, d=1)     # Frequências associadas (d=1 porque é diário)
amplitude = np.abs(fft)

# Considerar só frequências positivas
mask = freq > 0
freq = freq[mask]
amplitude = amplitude[mask]

# Converter frequência para período (em dias)
periodo = 1 / freq

# Plotar
plt.figure(figsize=(10, 5))
plt.plot(periodo, amplitude, color="purple")
plt.title("Análise de Frequência (FFT) - Casos Diários de Dengue")
plt.xlabel("Período (dias)")
plt.ylabel("Amplitude")
plt.xlim(2, 60)  # Foco em ciclos relevantes
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
