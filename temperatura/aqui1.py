import pandas as pd
import matplotlib.pyplot as plt
import PathManager

# Parâmetros principais
parametro_data = "DT_SIN_PRI"
parametro_codigo_municipio = "ID_MN_RESI"

# Parâmetros adicionais
colunas_necessarias = [
    parametro_data,
    parametro_codigo_municipio,
    "NU_IDADE_N",
    "CS_SEXO",
    "FEBRE",
    "MIALGIA",
    "CEFALEIA",
    "EXANTEMA",
    "VOMITO",
    "NAUSEA",
    "DOR_COSTAS",
]

# Define os tipos como string (exceto a data, que será convertida automaticamente)
dtype_colunas = {col: "string" for col in colunas_necessarias if col != parametro_data}

# Lê o CSV
df_dengue = pd.read_csv(
    PathManager.dengue_file,
    dtype=dtype_colunas,
    parse_dates=[parametro_data],
    usecols=colunas_necessarias,
)

# Filtro por ano de 2024
df_dengue_2024 = df_dengue[df_dengue[parametro_data].dt.year == 2024]

# Dicionário de cidades (ID: Nome)
cidades = {
    420540: "florianopolis",
    421190: "palhoca",
    421660: "saojose"
}

# Gera um CSV para cada cidade
for cod_cidade, nome_cidade in cidades.items():
    df_cidade = df_dengue_2024[df_dengue_2024[parametro_codigo_municipio] == str(cod_cidade)].copy()
    
    # Remove o prefixo "40" da idade
    df_cidade["NU_IDADE_N"] = df_cidade["NU_IDADE_N"].str.replace(r"^40", "", regex=True)

    # Remove a coluna do município
    df_cidade = df_cidade.drop(columns=[parametro_codigo_municipio])

    # Ordena por data
    df_cidade = df_cidade.sort_values(by=parametro_data)

    # Salva CSV
    df_cidade.to_csv(f"{nome_cidade}_2024.csv", index=False)
