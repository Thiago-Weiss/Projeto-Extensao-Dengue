import os


# Diretório raiz
raiz = "temperatura"
os.makedirs(raiz, exist_ok=True)



# Diretórios de dados brutos
dadosBrutos = os.path.join(raiz, "dadosBrutos")
os.makedirs(dadosBrutos, exist_ok=True)



coordenadasBrutos_dir = os.path.join(dadosBrutos, "coordenadas")
os.makedirs(coordenadasBrutos_dir, exist_ok=True)

temperaturaBrutos_dir = os.path.join(dadosBrutos, "temperatura")
os.makedirs(temperaturaBrutos_dir, exist_ok=True)

dengueBruto_dir = os.path.join(dadosBrutos, "dengue")
os.makedirs(dengueBruto_dir, exist_ok=True)



# Diretórios de dados tratados
dadosTratados = os.path.join(raiz, "dadosTratados")
os.makedirs(dadosTratados, exist_ok=True)


coordenadasTratadas_dir = os.path.join(dadosTratados, "coordenadas")
os.makedirs(coordenadasTratadas_dir, exist_ok=True)

temperaturaTratadas_dir = os.path.join(dadosTratados, "temperatura")
os.makedirs(temperaturaTratadas_dir, exist_ok=True)

dengueTratada_dir = os.path.join(dadosTratados, "dengue")
os.makedirs(dengueTratada_dir, exist_ok=True)



# diretorio dos dados agrupados
dadosAgrupados_dir = os.path.join(raiz, "dadosAgrupados")
os.makedirs(dadosAgrupados_dir, exist_ok=True)



# log file
logs_dir = os.path.join(raiz, "logs")
os.makedirs(logs_dir, exist_ok=True)



# files de 2024
log_file = os.path.join(logs_dir, "log.txt")
indexTemperatura_file = os.path.join(temperaturaTratadas_dir, "__index.csv")
indexTemperaturaProcesada_file = os.path.join(temperaturaTratadas_dir, "__index_processado.csv")
municipios_file = os.path.join(coordenadasBrutos_dir, "RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls")
cacheCidades_file = os.path.join(coordenadasBrutos_dir, "cache_cidades.csv")
dengue_file = os.path.join(dengueBruto_dir, "DENGBR24.csv")







