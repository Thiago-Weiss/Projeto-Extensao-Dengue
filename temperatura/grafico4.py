import pandas as pd
import matplotlib.pyplot as plt
import PathManager
import itertools

# Criar intervalo de datas do ano todo
ano = 2024


# Códigos dos municípios
saojose 		= 421660
florianopolis 	= 420540
palhoca       	= 421190
biguacu		    = 420230

cidades = [saojose, florianopolis, palhoca, biguacu,]

# Mapear nomes das cidades
mapa_cidades = {
    saojose: "São José",
    florianopolis: "Florianópolis",
    palhoca: "Palhoça",
    biguacu: "Biguaçu",
}





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




df_cidades = df_dengue[df_dengue[parametro_codigo_municipio].isin(cidades)].copy()

# Agrupar por data e cidade e contar os casos por dia
df_agrupado = df_cidades.groupby([parametro_data, parametro_codigo_municipio]).size().reset_index(name="Casos")

# Criar todas as combinações de (data, cidade)
datas = pd.date_range(start=f"{ano}-01-01", end=f"{ano}-12-31", freq="D")
combinacoes = pd.DataFrame(
    list(itertools.product(datas, cidades)),
    columns=[parametro_data, parametro_codigo_municipio]
)

# Fazer o merge para incluir todos os dias e cidades (mesmo sem casos)
df_completo = combinacoes.merge(df_agrupado, on=[parametro_data, parametro_codigo_municipio], how="left")

# Preencher os NaNs (sem casos) com 0
df_completo["Casos"] = df_completo["Casos"].fillna(0).astype(int)

df_completo.to_csv("teste.csv")

# Pivotar para ter colunas por cidade
df_pivot = df_completo.pivot(index=parametro_data, columns=parametro_codigo_municipio, values="Casos").fillna(0)

# Plotar
plt.figure(figsize=(14, 6))

df_pivot.plot(ax=plt.gca(), linewidth=2)

plt.title("Casos Diários de Dengue por Cidade")
plt.xlabel("Data")
plt.ylabel("Número de Casos")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.legend(title="Cidade")

# Mostrar total de casos no ano por cidade
totais = df_cidades[parametro_codigo_municipio].value_counts()
for cidade, total in totais.items():
    print(f"{cidade}: {total} casos no ano")

plt.show()
