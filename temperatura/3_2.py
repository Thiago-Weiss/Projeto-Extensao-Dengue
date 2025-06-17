import pandas as pd
import PathManager

# Parâmetros
pathSintomas = "regiaoCidadeSintomas.csv"

# Códigos dos municípios
saojose 		= 421660
florianopolis 	= 420540
palhoca       	= 421190
biguacu		    = 420230

cidades = [saojose, florianopolis, palhoca, biguacu]

# Mapear nomes das cidades
mapa_cidades = {
    saojose: "São José",
    florianopolis: "Florianópolis",
    palhoca: "Palhoça",
    biguacu: "Biguaçu",
}

# Campos desejados
parametro_codigo_municipio = "ID_MN_RESI"
campos_desejados = {
    "CS_SEXO": {
        "M": "SEXO_Masculino",
        "F": "SEXO_Feminino",
    },
    "FEBRE": {
        1: "FEBRE_Sim",
        2: "FEBRE_Nao",
    },
    "VOMITO": {
        1: "VOMITO_Sim",
        2: "VOMITO_Nao",
    },
    "MIALGIA": {
        1: "MIALGIA_Sim",
        2: "MIALGIA_Nao",
    },
    "CEFALEIA": {
        1: "CEFALEIA_Sim",
        2: "CEFALEIA_Nao",
    },
    "EXANTEMA": {
        1: "EXANTEMA_Sim",
        2: "EXANTEMA_Nao",
    },
    "NAUSEA": {
        1: "NAUSEA_Sim",
        2: "NAUSEA_Nao",
    },
    "DOR_COSTAS": {
        1: "DOR_COSTAS_Sim",
        2: "DOR_COSTAS_Nao",
    },
}

# Leitura do arquivo dengue
colunas_necessarias = list(campos_desejados.keys()) + [parametro_codigo_municipio]
df = pd.read_csv(
    PathManager.dengue_file,
    usecols=colunas_necessarias,
    dtype={parametro_codigo_municipio: "Int64"},
)

# Filtrar apenas cidades desejadas
df = df[df[parametro_codigo_municipio].isin(cidades)].copy()
df["Cidade"] = df[parametro_codigo_municipio].map(mapa_cidades)

# Contar total de casos por cidade
df_total = df.groupby("Cidade").size().rename("TotalCasos")

# Inicializar dicionário para contagens por sintoma/sexo/etc.
contagens = {}

for campo, mapeamento in campos_desejados.items():
    for valor, nome_coluna in mapeamento.items():
        contagem = df[df[campo] == valor].groupby("Cidade").size()
        contagens[nome_coluna] = contagem

# Juntar contagens + total de casos
df_resultado = pd.DataFrame(contagens).fillna(0).astype(int)
df_resultado.insert(0, "TotalCasos", df_total)
df_resultado = df_resultado.reset_index()  # Cidade vira a primeira coluna

# Salvar CSV
df_resultado.to_csv(pathSintomas, index=False)
print(f"✅ Arquivo salvo com total de casos em: {pathSintomas}")
