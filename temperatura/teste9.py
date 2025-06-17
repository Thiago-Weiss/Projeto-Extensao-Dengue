import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar dados
arquivo = 'temperatura/dadosAgrupados/dado1.csv'
df = pd.read_csv(arquivo, skiprows=2)

df['DATA'] = pd.to_datetime(df['DATA'])
casos = df['casos'].values

# FFT da série de casos
fft_vals = np.fft.fft(casos)
freqs = np.fft.fftfreq(len(casos), d=1)  # d=1 dia

# Evitar divisão por zero
freqs_nonzero = freqs.copy()
freqs_nonzero[freqs_nonzero == 0] = 1e-10

periodos = 1 / np.abs(freqs_nonzero)

# Frequências correspondentes a períodos entre 3 e 15 dias
mask = (periodos >= 3) & (periodos <= 15)

# Criar filtro passa-banda: mantém FFT só nas frequências do intervalo
fft_filtrado = np.zeros_like(fft_vals, dtype=complex)
fft_filtrado[mask] = fft_vals[mask]
fft_filtrado[~mask] = fft_vals[~mask]  # simetria da FFT corrigida

# Sinal filtrado no domínio do tempo (reconstrução)
sinal_filtrado = np.fft.ifft(fft_filtrado).real

# Plot
plt.figure(figsize=(12,6))
plt.plot(df['DATA'], casos, label='Casos Originais')
plt.plot(df['DATA'], sinal_filtrado, label='Oscilação 3-15 dias (Filtro FFT)', linewidth=2)
plt.xlabel('Data')
plt.ylabel('Casos')
plt.title('Casos Diários com Oscilações Filtradas (3 a 15 dias)')
plt.legend()
plt.grid(True)
plt.show()
