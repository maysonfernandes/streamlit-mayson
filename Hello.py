import streamlit as st
import matplotlib.pyplot as plt

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
# import plotly.graph_objects as go
from datetime import datetime

st.set_option('deprecation.showPyplotGlobalUse', False)


st.set_page_config(page_title='Análise de Dados das Ações do IBOV')

# Configurando a Sidebar
dia_inicial = st.sidebar.slider('Dia inicial', min_value=1,max_value=31)
mes_inicial = st.sidebar.selectbox('Mês Inicial', ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
ano_inicial = st.sidebar.selectbox('Ano Inicial', (2024, 2023, 2022, 2021, 2020))
st.sidebar.write('---')
dia_final = st.sidebar.slider('Dia Final', min_value=1,max_value=31, value=31)
mes_final = st.sidebar.selectbox('Mês Final', ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
ano_final = st.sidebar.selectbox('Ano Final', (2024, 2023, 2022, 2021, 2020))
meses_string = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
meses_numeros = {mes: i+1 for i, mes in enumerate(meses_string)}
numero_mes_inicial = meses_numeros.get(mes_inicial.lower(), None)
numero_mes_final = meses_numeros.get(mes_final.lower(), None)
start = datetime.strptime(f'{ano_inicial}-{numero_mes_inicial}-{dia_inicial}', "%Y-%m-%d")
end = datetime.strptime(f'{ano_final}-{numero_mes_final}-{dia_final}', "%Y-%m-%d")
if start > end:
   st.sidebar.error("Erro (ano menor que o inicio)")
else:
   st.sidebar.success('datas verificadas')

# Definindo as Configurações básicas
periodo = '1d' #
ibov = 'IBOVDia_15-03-24.csv' # Nome do arquivo do IBOV
filtro = 5 # Quantidade de empresas para filtro de Ranking

# Abrindo o arquivo CSV com as empresas que compõe o IBOV
dados = pd.read_csv(ibov, sep=';', header=1, encoding='latin-1', index_col=False)
dados.drop([dados.shape[0] -2, dados.shape[0]-1], inplace=True)

# Criando uma lista com os Tickers para a busca dos dados no yfinance
tikers = []
for codigo in dados['Código']:
    tikers.append(f'{codigo}.SA')

# Buscando os dados diários para o periodo informado de cada empresa do IBOV
dados_acoes = yf.download(tikers, period=periodo, start=start,end=end)

def grafico(x,y,nome_grafico):
  fig, ax = plt.subplots()
  ax = plt.figure(figsize=(12,5))
  ax = plt.xlabel('Data')
  ax = plt.ylabel('Preço')
  ax = plt.title(nome_grafico)
  fig = plt.plot(x, y, linewidth=0.8)

def grafico_legenda(x,y,nome_grafico, tickers_destaque):
  fig, ax = plt.subplots()
  ax = plt.figure(figsize=(12,5))
  ax = plt.xlabel('Data')
  ax = plt.ylabel('Preço')
  ax = plt.title(nome_grafico)
  fig = plt.plot(x, y, linewidth=1.5)
  ax = plt.legend(list(tickers_destaque), fontsize=8)
 

# Plotando o Gráfico com todas as ações

# Normalizando os dados das Ações
dados_normalizados = dados_acoes['Adj Close'] / dados_acoes['Adj Close'].iloc[0]

# Plotando o Gráfico com os dados Normalizados
grafico(dados_acoes.index, dados_normalizados, 'Todas as Ações do IBOV - Dados Normalizados')

# Criando uma lista com as 10 empresas com maior ganho no periodo
lista = []
for i in dados_normalizados:
    lista.append([i,dados_normalizados[i][-1]])
lista = pd.DataFrame(lista).sort_values(by=1,ascending=False)
lista.columns = ['Ticker', 'V_final']
tickers_destaque = lista['Ticker'].iloc[0:filtro]

# Buscando os dados para as empresas destaque no yfinance
dados_acoes_destaque = yf.download(list(tickers_destaque), period=periodo, start=start, end=end)

# Normalizando os dados das empresas destaque
dados_normalizados_destaque = dados_acoes_destaque['Adj Close'] / dados_acoes_destaque['Adj Close'].iloc[0]

# Plotando um Gráfico com os dados normalizados das empresas destaque
grafico(dados_acoes_destaque.index, dados_normalizados_destaque, f'Ranking das {filtro} Ações do IBOV com Melhor Desempenho')
plt.legend(list(tickers_destaque), fontsize=8)
            
lista = []
for i in dados_normalizados:
    lista.append([i,dados_normalizados[i][-1]])
lista = pd.DataFrame(lista).sort_values(by=1,ascending=True)
lista.columns = ['Ticker', 'V_final']
tickers_destaque_neg = lista['Ticker'].iloc[0:filtro]

# Buscando os dados para as empresas destaque no yfinance
dados_acoes_destaque_neg = yf.download(list(tickers_destaque_neg), period='1d', start=start, end=end)

# Normalizando os dados das empresas destaque
dados_normalizados_destaque_neg = dados_acoes_destaque_neg['Adj Close'] / dados_acoes_destaque_neg['Adj Close'].iloc[0]

# Plotando um Gráfico com os dados normalizados das empresas menos destacadas
grafico(dados_acoes_destaque_neg.index, dados_normalizados_destaque_neg, f'Ranking das {filtro} Ações do IBOV com Pior Desempenho')
plt.legend(list(tickers_destaque_neg), fontsize=8)






with st.container():
    st.title('Analizando os dados das ações do indice IBOV')
    st.subheader('Utilizando Python para recuperar os dados das ações do Índice IBOV, iremos representar graficamente sua evolução ao longo do período selecionado, além de criar um ranking que destaque as empresas com melhor e pior desempenho.')
    st.text('''
    # Importando as Bibliotecas necessárias
    import yfinance as yf
    import matplotlib.pyplot as plt
    import pandas as pd
    import plotly.graph_objects as go
    from datetime import datetime

    # Definindo as Configirações básicas
    periodo = '1d' #
    start = '2023-01-01' # Data de Início dos dados
    final = '2023-12-31' # Data Final para busca dos Dados
    ibov = 'IBOVDia_15-03-24.csv' # Nome do arquivo do IBOV
    filtro = 5 # Quantidade de empresas para filtro de Ranking

    # Abrindo o arquivo CSV com as empresas que compõe o IBOV
    dados = pd.read_csv(ibov, sep=';', header=1, encoding='latin-1', index_col=False)
    dados.drop([dados.shape[0] -2, dados.shape[0]-1], inplace=True)

    # Criando uma lista com os Tickers para a busca dos dados no yfinance
    tikers = []
    for codigo in dados['Código']:
        tikers.append(f'{codigo}.SA')

    # Buscando os dados diários para o periodo informado de cada empresa do IBOV
    dados_acoes = yf.download(tikers, period=periodo, start=start,end=final)

    # Função para gerar os Gráficos 
    def grafico(x,y,nome_grafico):
        ax = plt.figure(figsize=(12,5))
        ax = plt.xlabel('Data')
        ax = plt.ylabel('Preço')
        ax = plt.title(nome_grafico)
        ax=plt.plot(x, y, linewidth=0.8)
    
    # Plotando o Gráfico com todas as ações
    grafico(dados_acoes.index, dados_acoes['Adj Close'], 'Todas as Ações do IBOV')
    ''')
    st.pyplot(grafico(dados_acoes.index, dados_acoes['Adj Close'], 'Todas as Ações do IBOV'))

    st.text('''
    # Normalizando os dados das Ações
    dados_normalizados = dados_acoes['Adj Close'] / dados_acoes['Adj Close'].iloc[0]

    # Plotando o Gráfico com os dados Normalizados
    grafico(dados_acoes.index, dados_normalizados, 'Todas as Ações do IBOV - Dados Normalizados')
    ''')

    st.pyplot(grafico(dados_acoes.index, dados_normalizados, 'Todas as Ações do IBOV - Dados Normalizados'))

    st.text('''
    # Criando uma lista com as empresas com maior ganho no periodo
    lista = []
    for i in dados_normalizados:
        lista.append([i,dados_normalizados[i][-1]])
    lista = pd.DataFrame(lista).sort_values(by=1,ascending=False)
    lista.columns = ['Ticker', 'V_final']
    tickers_destaque = lista['Ticker'].iloc[0:filtro]

    # Buscando os dados para as empresas destaque no yfinance
    dados_acoes_destaque = yf.download(list(tickers_destaque), period=periodo, start=start, end=final)

    # Normalizando os dados das empresas destaque
    dados_normalizados_destaque = dados_acoes_destaque['Adj Close'] / dados_acoes_destaque['Adj Close'].iloc[0]
    
    # Plotando um Gráfico com os dados normalizados das empresas destaque
    grafico(dados_acoes_destaque.index, dados_normalizados_destaque, f'Ranking das {filtro} Ações do IBOV com Melhor Desempenho')
    plt.legend(list(tickers_destaque), fontsize=8)
    ''')

    st.pyplot(grafico_legenda(dados_acoes_destaque.index, dados_normalizados_destaque, f'Ranking das {filtro} Ações do IBOV com Melhor Desempenho', tickers_destaque))

    st.text('''
    # Criando uma lista com os Tickers das empresas com poir desempenho
    lista = []
    for i in dados_normalizados:
        lista.append([i,dados_normalizados[i][-1]])
    lista = pd.DataFrame(lista).sort_values(by=1,ascending=True)
    lista.columns = ['Ticker', 'V_final']
    tickers_destaque_neg = lista['Ticker'].iloc[0:filtro]

    # Buscando os dados para as empresas destaque no yfinance
    dados_acoes_destaque_neg = yf.download(list(tickers_destaque_neg), period='1d', start=start, end=final)

    # Normalizando os dados das empresas destaque
    dados_normalizados_destaque_neg = dados_acoes_destaque_neg['Adj Close'] / dados_acoes_destaque_neg['Adj Close'].iloc[0]

    # Plotando um Gráfico com os dados normalizados das empresas menos destacadas
    grafico(dados_acoes_destaque_neg.index, dados_normalizados_destaque_neg, f'Ranking das {filtro} Ações do IBOV com Pior Desempenho')
    plt.legend(list(tickers_destaque_neg), fontsize=8)
    ''')

    st.pyplot(grafico_legenda(dados_acoes_destaque_neg.index, dados_normalizados_destaque_neg, f'Ranking das {filtro} Ações do IBOV com Pior Desempenho', tickers_destaque=tickers_destaque_neg ))


with st.container():
  st.write('---')
  st.text('Copyright © 2024, Mayson Fernandes')