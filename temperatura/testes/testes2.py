import pandas as pd

# Lê os arquivos
df2 = pd.read_csv('temperatura/dengue/DENGBR23.csv', low_memory=False, usecols= ['ID_MUNICIP'])
qtd_municipios = df2["ID_MUNICIP"].nunique()
print("Quantidade de municípios diferentes:", qtd_municipios)
df1 = pd.read_csv('temperatura/processados/dado6.csv', parse_dates=['DATA'])

print(df2.shape)
# Garante que a coluna de município está no formato string, sem espaços
df2["ID_MUNICIP"] = df2["ID_MUNICIP"].astype(str).str.strip()
print("Total de linhas em df2:", df2.shape[0])


# Define o código do município desejado (ex: "520001")
codigo_municipio = "120020"

# Filtra df2 apenas para esse município
df2_filtrado = df2[df2["ID_MUNICIP"] == codigo_municipio].copy()
print(f"Total de linhas em df2_filtrado para o município {codigo_municipio}:", df2_filtrado.shape[0])

df1['DATA'] = pd.to_datetime(df1['DATA']).dt.normalize()
df2_filtrado.loc[:, 'DT_NOTIFIC'] = pd.to_datetime(df2_filtrado['DT_NOTIFIC']).dt.normalize()


df2_filtrado['ANO_NASC'] = df2_filtrado['ANO_NASC'].astype(int)
contagems = df2_filtrado.groupby('DT_NOTIFIC').agg(
    contagem_x=('DT_NOTIFIC', 'size'),
    anos=('ANO_NASC', 'sum')
).reset_index()

print(contagems[:10])

# Conta quantas linhas existem por data (já filtrado pelo município)
contagem = df2_filtrado.groupby('DT_NOTIFIC').size().reset_index(name='contagem_x')
contagem.rename(columns={'DT_NOTIFIC': 'DATA'}, inplace=True)
print(f"casos {codigo_municipio}:", contagem.shape[0])




# Junta com df1 pelas datas
df_resultado = pd.merge(df1, contagem, on=' ', how='left')

# Preenche com 0 onde não houve registros
df_resultado['contagem_x'] = df_resultado['contagem_x'].fillna(0).astype(int)

# (Opcional) salva o resultado
df_resultado.to_csv('arquivo_completo.csv', index=False)
