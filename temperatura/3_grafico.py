import pandas as pd
import matplotlib.pyplot as plt
import PathManager

# Parâmetros
ano = 2024
mes_inicio = 1
mes_fim = 12
pathSave = "regiaoCidadeCasos.csv"

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


parametro_data = "DT_SIN_PRI"
parametro_codigo_municipio = "ID_MN_RESI"

colunas_necessarias = [parametro_data, parametro_codigo_municipio]



# Leitura do arquivo
df_dengue = pd.read_csv(
    PathManager.dengue_file,
    parse_dates=[parametro_data],
    usecols=colunas_necessarias,
    dtype={parametro_codigo_municipio: "Int64"},
)

# Filtrar somente as cidades desejadas
df_cidades = df_dengue[df_dengue[parametro_codigo_municipio].isin(cidades)].copy()

# Adicionar nomes das cidades
df_cidades["Cidade"] = df_cidades[parametro_codigo_municipio].map(mapa_cidades)

# Agrupar por data e cidade e contar os casos
df_agrupado = df_cidades.groupby([parametro_data, "Cidade"]).size().reset_index(name="Casos")

# Criar todas as datas do ano como DataFrame base
datas_ano = pd.date_range(start=f"{ano}-01-01", end=f"{ano}-12-31", freq="D")
df_datas = pd.DataFrame({parametro_data: datas_ano})

# Pivotar o agrupado: datas como índice, cidades como colunas
df_pivot = df_agrupado.pivot(index=parametro_data, columns="Cidade", values="Casos")

# Juntar com datas para garantir todos os dias do ano
df_final = df_datas.merge(df_pivot, on=parametro_data, how="left").fillna(0)


# Converter coluna a coluna para int
for col in df_final.columns[1:]:
    df_final[col] = df_final[col].astype(int)


df_final.to_csv(pathSave, index= False)




# Filtrar entre os meses desejados
df_filtrado = df_final[
    df_final[parametro_data].dt.month.between(mes_inicio, mes_fim)
]

for cidade in df_filtrado.columns[1:]:  # Ignora a coluna de data
    plt.figure(figsize=(12, 5))
    plt.scatter(df_filtrado[parametro_data], df_filtrado[cidade], label=cidade, s=10)
    plt.title(f"Casos Diários de Dengue em {cidade} (meses {mes_inicio} a {mes_fim})")
    plt.xlabel("Data")
    plt.ylabel("Número de Casos")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()





