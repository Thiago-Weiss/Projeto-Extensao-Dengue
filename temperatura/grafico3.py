import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PathManager

# --- Suponha que esses parâmetros já estão definidos ---
parametro_data = "DT_SIN_PRI"
parametro_codigo_municipio = "ID_MN_RESI"

colunas_necessarias = [
    parametro_data,
    parametro_codigo_municipio,
]

# Códigos dos municípios
florianopolis = 420540 
palhoca       = 421190 
saoJose       = 421660

# Leitura do arquivo
df_dengue = pd.read_csv(
    PathManager.dengue_file,
    parse_dates=[parametro_data],
    usecols=colunas_necessarias,
    dtype={parametro_codigo_municipio: "Int64"},
)

# --- Filtrar as 3 cidades (ou só uma, se quiser) ---
municipios_interesse = [420540, 421190, 421660]  # Florianópolis, Palhoça, São José
df_cidades = df_dengue[df_dengue[parametro_codigo_municipio].isin(municipios_interesse)]

# --- Filtrar período de fevereiro a julho ---
df_periodo = df_cidades[
    (df_cidades[parametro_data].dt.month >= 2) &
    (df_cidades[parametro_data].dt.month <= 7)
]

# --- Contar casos por dia ---
serie_diaria = df_periodo.groupby(parametro_data).size()

# --- Transformada de Fourier ---
y = serie_diaria.values
n = len(y)

fft = np.fft.fft(y - np.mean(y))       # Remove a média (centraliza)
freq = np.fft.fftfreq(n, d=1)          # Frequências (1 ponto por dia)
amplitude = np.abs(fft)

# --- Filtrar só frequências positivas ---
mask = freq > 0
freq = freq[mask]
amplitude = amplitude[mask]
periodo = 1 / freq  # Em dias

# --- Plotar o gráfico ---
plt.figure(figsize=(10, 5))
plt.plot(periodo, amplitude, color="purple")
plt.title("Transformada de Fourier - Casos Diários de Dengue (Fev–Jul)")
plt.xlabel("Período (dias)")
plt.ylabel("Amplitude")
plt.xlim(2, 60)  # Foco em ciclos de até 2 meses
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
