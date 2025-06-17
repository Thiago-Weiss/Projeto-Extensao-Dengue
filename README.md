
# 🦟 Projeto de Extensão — Análise da Dengue e Correlação com o Clima

Este projeto tem como objetivo realizar uma **análise estatística da ocorrência de casos de dengue e sua possível correlação com fatores climáticos**. Foram utilizados dados de casos de dengue em diferentes cidades e dados climáticos (temperatura) para geração de gráficos e análises.

Os resultados foram representados tanto em **gráficos gerados com Python (via matplotlib e pandas)** quanto em **dashboards interativos feitos no Power BI**.

---

## 📁 Arquivos do Projeto

### 🔹 Arquivos Principais Utilizados:

- **`3_grafico.py`**  
  → Gera gráficos de **Casos de Dengue por Cidade ao longo do ano**.  
  → Dados de saída: **`regiaoCidadeCasos.csv`** (usado também no Power BI).

- **`3_2.py`**  
  → Gera gráficos de **Cidades x Sintomas reportados**.  
  → Dados de saída: **`regiaoCidadeSintomas.csv`** (usado no Power BI).

- **`3_3.py`**  
  → Gera gráficos do **Clima (temperatura) ao longo do ano nas cidades**.  
  → Dados de saída: **`regiaoTemperatura.csv`** (usado no Power BI).

---

### 🔸 Arquivos de Processamento Descartados (Escala Nacional):

Estes arquivos foram desenvolvidos para trabalhar com dados em nível nacional, mas foram descartados por questão de tempo e foco do projeto.

- **`1_processarTemperaturas.py`**  
  → Processa mais de **500 arquivos CSV de temperaturas** do Brasil.  
  → Move os dados de `temperatura/dadosBrutos/temperatura` para `temperatura/dadosTratados/temperatura`.  
  → Gera o arquivo **`__index.csv`** contendo o nome do arquivo e suas respectivas **coordenadas geográficas (latitude e longitude)**.

- **`2_cordenadas2CidadeUF.py`**  
  → Converte as **coordenadas geográficas para Cidade e Estado**, utilizando a API do OpenStreetMap:  
  https://nominatim.openstreetmap.org/reverse

---

### 🗂️ Outros Arquivos

Os demais arquivos presentes no repositório são utilizados para testes, rascunhos ou scripts auxiliares.

---

## 📊 Visualizações

Foram gerados dois tipos principais de visualizações:

- **Gráficos em Python:**  
  Utilizando `matplotlib` e `pandas` para análises rápidas e exploração dos dados.

- **Dashboards no Power BI:**  
  Utilizando os arquivos CSV exportados pelos scripts Python para criar dashboards interativos e análises mais detalhadas.

---

## 🧠 Bibliotecas Utilizadas

- **`pandas`** → Manipulação de dados e DataFrames  
- **`csv`** → Leitura e escrita de arquivos CSV  
- **`requests`** → Requisições HTTP para API geográfica  
- **`matplotlib.pyplot`** → Geração de gráficos  

API utilizada para geolocalização:  
https://nominatim.openstreetmap.org/reverse

---

## 🔗 Repositório no GitHub

[https://github.com/Thiago-Weiss/Projeto-Extensao-Dengue](https://github.com/Thiago-Weiss/Projeto-Extensao-Dengue)
