import os
import pandas as pd
import PathManager
import LogManager

# colunas do csv
parametro_data = "Data"
parametro_precipitacao = "PRECIPITAÇÃO TOTAL, HORÁRIO (mm)"
parametro_temperatura = "TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"
parametro_umidade = "UMIDADE RELATIVA DO AR, HORARIA (%)"

colunas_necessarias = [
    parametro_data,
    parametro_precipitacao,
    parametro_temperatura,
    parametro_umidade
]


# colunas dos dados exportado/processados
p_e_data = "DATA"
p_e_chuva = "CHUVA"
p_e_temp_max = "TEMP MAX GRAUS"
p_e_tem_min = "TEMP MIN GRAUS"
p_e_umid_max = "UMID MAX PORCENTAGEM"
p_e_umid_min= "UMID MIN PORCENTAGEM"




# pega todos os arquivos .csv
arquivos = sorted([f for f in os.listdir(PathManager.temperaturaBrutos_dir) if f.lower().endswith('.csv')])


# reescreve o index.csv
with open(PathManager.indexTemperatura_file, "w", encoding="utf-8") as info:
    info.write("ARQUIVO,LATITUDE,LONGITUDE\n")



i = 0
for nome_arquivo in (arquivos):
    caminho_arquivo = os.path.join(PathManager.temperaturaBrutos_dir, nome_arquivo)

    try:
        with open(caminho_arquivo, encoding='ISO-8859-1') as f:
            linhas = f.readlines()

        
        # Extrair cabeçalho
        latitude = longitude = None
        for linha in linhas[:10]:
            if linha.startswith("LATITUDE:"):
                latitude = linha.replace("LATITUDE:;", "").strip().replace(',', '.')
                latitude = float(latitude)

            elif linha.startswith("LONGITUDE:"):
                longitude = linha.replace("LONGITUDE:;", "").strip().replace(',', '.').strip()
                longitude = float(longitude)


        # se nao achar a cordenadas pula esse arquivo
        if (not latitude) or (not longitude):
            LogManager.write_log(f"[Erro] nao achou a latitude: {latitude} ou a longitude: {longitude}")
            continue


        # Localiza onde começam os dados
        for idx, linha in enumerate(linhas):
            if linha.strip().startswith("Data"):
                header_idx = idx
                break


        # Lê tabela
        try:
            df = pd.read_csv(
                caminho_arquivo,
                skiprows=header_idx,
                encoding='ISO-8859-1',
                sep=';',
                decimal=',',
                usecols=colunas_necessarias,
                parse_dates=[parametro_data],
                dtype={
                    parametro_precipitacao: "float",
                    parametro_temperatura: "float",
                    parametro_umidade: "float"
                },
                on_bad_lines='skip')
        except Exception as e:
            print(e)
            LogManager.write_log(f"Erro ao ler {caminho_arquivo}: {e}")
            continue

        # Ignora linhas sem data
        df = df.dropna(subset=[parametro_precipitacao, parametro_temperatura, parametro_umidade], how='any')



        df["DIA"] = df[parametro_data].dt.date

        # Inicializa lista de resultados
        resumo = []

        for dia, grupo in df.groupby("DIA"):
            chuva = grupo[parametro_precipitacao].sum()
            chuva = round(chuva, 2)

            temp = grupo[parametro_temperatura]
            temp_max = round(temp.max(), 2)
            temp_min = round(temp.min(), 2)

            umid = grupo[parametro_umidade]
            umid_max = round(umid.max(), 2)
            umid_min = round(umid.min(), 2)

            resumo.append({
                p_e_data: dia,
                p_e_chuva: chuva,
                p_e_temp_max: temp_max,
                p_e_tem_min: temp_min,
                p_e_umid_max: umid_max,
                p_e_umid_min: umid_min
            })


        if not resumo or len(resumo) < 330:
            LogManager.write_log(f"[ERRO] Arquivo '{nome_arquivo}' ignorado: Somente {len(resumo)} dias com dados.\n")
            continue


        # Depois do seu loop que cria o resumo
        df_resumo = pd.DataFrame(resumo)
        df_resumo[p_e_data] = pd.to_datetime(df_resumo[p_e_data])


        # Extrai o ano das datas (assumindo que todas são do mesmo ano)
        ano = df_resumo[p_e_data].dt.year.iloc[0]

        # Define o intervalo completo do ano
        data_inicio = pd.Timestamp(f"{ano}-01-01")
        data_fim = pd.Timestamp(f"{ano}-12-31")
        datas_completas = pd.date_range(start=data_inicio, end=data_fim, freq='D')


        # Reindexa o DataFrame para ter todos os dias no intervalo
        df_resumo = df_resumo.set_index(p_e_data).reindex(datas_completas)
        df_resumo.index.name = p_e_data
        df_resumo = df_resumo.reset_index()

  

        i += 1
        novo_nome = f"dado{i}.parquet"
        novo_caminho = os.path.join(PathManager.temperaturaTratadas_dir, novo_nome)
        df_resumo.to_parquet(novo_caminho, index=False)


        # Salva info
        with open(PathManager.indexTemperatura_file, "a", encoding="utf-8") as info:
            info.write(f"{novo_nome},{latitude},{longitude}\n")


        # limpa a tela no Windows (cls) ou Unix (clear)
        os.system('cls' if os.name == 'nt' else 'clear')  
        print(f"arquivo [{i} -> {len(arquivos)}] ({(i/len(arquivos))*100:.2f}%)")


    except Exception as e:
        LogManager.write_log(f"[ERRO] Arquivo '{caminho_arquivo}': Nao foi possivel abrir")
        continue

