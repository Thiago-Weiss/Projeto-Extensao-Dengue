import requests
import pandas as pd
import os
import csv
from time import sleep
import unidecode
import PathManager
import LogManager


# colunas do csv
parametro_nome_municipio = "Nome_Município"
parametro_nome_uf = "Nome_UF"
parametro_codigo_regiao_imediata = "Região Geográfica Imediata"
parametro_codigo_municipio = "Código Município Completo"

colunas_necessarias = [
    parametro_nome_municipio,
    parametro_nome_uf,
    parametro_codigo_regiao_imediata,
    parametro_codigo_municipio
]


# colunas dos dados uso interno
p_i_nome_municipio = "nome_municipio"
p_i_nome_uf = "nome_uf"
p_i_codigo_nome_municipio = "codigo_municipio_sem_dv"






tolerancia = 0.02
# tolerancia
# Casas Decimais	Aproximadamente 	Precisão em metros na superfície
# 0                 	1 grau              	~111 km
# 1	                    0,1 grau            	~11 km
# 2	                    0,01 grau           	~1,1 km
# 3	                    0,001 grau          	~110 m
# 4	                    0,0001 grau         	~11 m



# cordenada para nome uf cidade
def carregar_cache():
    if os.path.exists(PathManager.cacheCidades_file):
        return pd.read_csv(PathManager.cacheCidades_file)
    else:
        return pd.DataFrame(columns=["lat", "lon", "cidade", "estado"])

def salvar_cache(df):
    df.to_csv(PathManager.cacheCidades_file, index=False)


def buscar_no_cache_com_tolerancia(lat, lon, df_cache):
    cond_lat = (df_cache['lat'] >= lat - tolerancia) & (df_cache['lat'] <= lat + tolerancia)
    cond_lon = (df_cache['lon'] >= lon - tolerancia) & (df_cache['lon'] <= lon + tolerancia)
    resultados = df_cache[cond_lat & cond_lon]
    
    if not resultados.empty:
        # Pega o primeiro resultado encontrado — você pode aprimorar para o mais próximo, se quiser
        linha = resultados.iloc[0]
        return linha['cidade'], linha['estado']
    return None, None


def consulta_api(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'lat': lat,
        'lon': lon,
        'format': 'json',
        'addressdetails': 1
    }
    headers = {'User-Agent': 'meu-projeto-teste/1.0'}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        addr = dados.get("address", {})
        cidade = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality")
        estado = addr.get("state") or addr.get("region")
        return cidade, estado
    else:
        print("[ERRO] API de cordenadas nao respondeu 200")
        return None, None


def coordenadas_para_cidade(lat, lon):
    df_cache = carregar_cache()

    cidade, estado = buscar_no_cache_com_tolerancia(lat, lon, df_cache)
    if cidade and estado:
        return cidade, estado

    cidade, estado = consulta_api(lat, lon)
    if cidade and estado:
        nova_linha = pd.DataFrame([{"lat": lat, "lon": lon, "cidade": cidade, "estado": estado}])
        df_cache = pd.concat([df_cache, nova_linha], ignore_index=True)
        salvar_cache(df_cache)
        sleep(1)
        return cidade, estado
    else:
        print("Erro ao buscar cidade.")

    return None, None














# uf e cidade para codigo da cidade e rigiao imediata
def padroniza_texto(texto):
    if texto is None:
        return None
    texto = str(texto).strip().lower()
    texto = unidecode.unidecode(texto)
    return texto



def busca_codigos_geograficos(cidade, estado):
    cidade = padroniza_texto(cidade)
    estado = padroniza_texto(estado)

    resultado = df_ibge[
        (df_ibge[p_i_nome_municipio] == cidade) &
        (df_ibge[p_i_nome_uf] == estado)
    ]

    if not resultado.empty:
        code_regiao = resultado.iloc[0][parametro_codigo_regiao_imediata]
        code_municipio = resultado.iloc[0][p_i_codigo_nome_municipio]
        return code_regiao, code_municipio
    else:
        LogManager.write_log("[ERRO] nao conseguiu achar a Região Geográfica Imediata ou o codigo do municipio")
        return None












# reseta o arquivo de index
if os.path.exists(PathManager.indexTemperaturaProcesada_file):
    os.remove(PathManager.indexTemperaturaProcesada_file)
with open(PathManager.indexTemperaturaProcesada_file, "a", encoding="utf-8") as indexFinal:
    indexFinal.write("ARQUIVO,CODIGO_REGIAO_IMEDIATA,CODIGO_MUNICIPIO,CIDADE,ESTADO\n")



# inicio o df do ibge fora uma unica vez (otimizaçao)
df_ibge = pd.read_excel(
    PathManager.municipios_file,
    skiprows=6,
    usecols=colunas_necessarias,
    dtype={
        parametro_nome_municipio: "string",
        parametro_nome_uf: "string",
        parametro_codigo_regiao_imediata: "Int64",
        parametro_codigo_municipio: "string"
    })

df_ibge.dropna(subset=[parametro_codigo_municipio], inplace=True)
df_ibge[p_i_codigo_nome_municipio] = df_ibge[parametro_codigo_municipio].str[:-1].astype("Int64")
df_ibge.dropna(subset=[p_i_codigo_nome_municipio], inplace=True)

# Padroniza colunas para evitar erros
df_ibge[p_i_nome_municipio] = df_ibge[parametro_nome_municipio].apply(padroniza_texto)
df_ibge[p_i_nome_uf] = df_ibge[parametro_nome_uf].apply(padroniza_texto)









# Abrir e processar cada linha
total_linhas = sum(1 for _ in open(PathManager.indexTemperatura_file)) - 1
with open(PathManager.indexTemperatura_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for i, linha in enumerate(reader, 1):
        try:
            
            # limpa a tela no Windows (cls) ou Unix (clear)
            os.system('cls' if os.name == 'nt' else 'clear')  
            print(f"linha [{i} -> {total_linhas}] ({(i/total_linhas)*100:.2f}%)")

            arquivo = linha["ARQUIVO"]
            lat = float(linha["LATITUDE"])
            lon = float(linha["LONGITUDE"])
            
            cidade, estado = coordenadas_para_cidade(lat, lon)
            if cidade and estado:
                code_regiao, code_municipio = busca_codigos_geograficos(cidade, estado)

                if code_regiao and code_municipio:
                    with open(PathManager.indexTemperaturaProcesada_file, "a", encoding="utf-8") as indexFinal:
                        indexFinal.write(f"{arquivo},{code_regiao},{code_municipio},{cidade},{estado}\n")

        except Exception as e:
        
            LogManager.write_log(f"[ERRO] nas cordenadas ou arquivo index\n")
            continue