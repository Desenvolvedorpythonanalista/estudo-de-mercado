import streamlit as st
import pandas as pd

# Dados das tabelas existentes
data_tabela_ticket_medio = {
    'Mercado/Indivíduo': ['Luciano Hang', 'Silvio Santos', 'Airbnb', 'Cibersegurança', 'Marketing Digital', 'Tecnologia de SaaS', 'Fintechs', 'Tecnologia de Saúde', 'Banco', 'Agronegócio'],
    'Faturamento Anual Global Estimado': ['~R$ 12 bilhões', '~R$ 3 bilhões (SBT e outros)', '~R$ 10 bilhões (2023)', '~R$ 220 bilhões (global)', '~R$ 600 bilhões (global)', '~R$ 750 bilhões (global)', '~R$ 500 bilhões (global)', '~R$ 250 bilhões (global)', '~R$ 6 trilhões (global)', '~R$ 7 trilhões (global)'],
    'Número Estimado de Consumidores/Transações': ['~100 milhões', '~10 milhões', '~100 milhões', '~5 milhões', '~1 bilhão', '~50 milhões', '~2 bilhões', '~1 bilhão', '~3 bilhões', '~1,5 bilhões'],
    'Ticket Médio Global Estimado': ['~R$ 120', '~R$ 300', '~R$ 100', '~R$ 44.000', '~R$ 600', '~R$ 15.000', '~R$ 250', '~R$ 250', '~R$ 2.000', '~R$ 4.667'],
    'Exemplos de Empresas': ['Havan', 'SBT, Sistema Brasileiro de Televisão', 'Airbnb', 'CrowdStrike, Palo Alto Networks', 'Google Ads, Meta Platforms', 'Salesforce, Microsoft Azure', 'Stripe, Square', 'Medtronic, Philips Healthcare', 'JPMorgan Chase, HSBC', 'Cargill, Bayer']
}

data_tabela_ticket_medio_nacional = {
    'Mercado/Indivíduo': ['Luciano Hang', 'Silvio Santos', 'Airbnb', 'Cibersegurança', 'Marketing Digital', 'Tecnologia de SaaS', 'Fintechs', 'Tecnologia de Saúde', 'Banco', 'Agronegócio'],
    'Faturamento Anual Nacional Estimado': ['~R$ 12 bilhões', '~R$ 3 bilhões (SBT e outros)', '~R$ 1,5 bilhões (Brasil)', '~R$ 6 bilhões (Brasil)', '~R$ 40 bilhões (Brasil)', '~R$ 80 bilhões (Brasil)', '~R$ 30 bilhões (Brasil)', '~R$ 25 bilhões (Brasil)', '~R$ 800 bilhões (Brasil)', '~R$ 1 trilhão (Brasil)'],
    'Número Estimado de Consumidores/Transações': ['~60 milhões', '~5 milhões', '~10 milhões', '~500 mil', '~150 milhões', '~10 milhões', '~400 milhões', '~150 milhões', '~500 milhões', '~300 milhões'],
    'Ticket Médio Nacional Estimado': ['~R$ 200', '~R$ 600', '~R$ 150', '~R$ 12.000', '~R$ 267', '~R$ 8.000', '~R$ 75', '~R$ 167', '~R$ 1.600', '~R$ 3.333'],
    'Exemplos de Empresas': ['Havan', 'SBT, Sistema Brasileiro de Televisão', 'Airbnb', 'Tempest, Kaspersky', 'Nubank, GuiaBolso', 'Totvs, Linx', 'PagSeguro, Stone', 'Dasa, Hapvida', 'Itaú Unibanco, Bradesco', 'Cargill, JBS']
}

data_tabela_global = {
    'Mercado/Indivíduo': ['Luciano Hang', 'Silvio Santos', 'Airbnb', 'Cibersegurança', 'Marketing Digital', 'Tecnologia de SaaS', 'Fintechs', 'Tecnologia de Saúde', 'Banco', 'Agronegócio'],
    'Faturamento Anual Global Estimado': ['~R$ 12 bilhões', '~R$ 3 bilhões (SBT e outros)', '~R$ 10 bilhões (2023)', '~R$ 220 bilhões (global)', '~R$ 600 bilhões (global)', '~R$ 750 bilhões (global)', '~R$ 500 bilhões (global)', '~R$ 250 bilhões (global)', '~R$ 6 trilhões (global)', '~R$ 7 trilhões (global)'],
    'Patrimônio Estimado': ['~R$ 2 bilhões', '~R$ 7 bilhões', '~R$ 35 bilhões', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', '~R$ 2 trilhões', 'N/A'],
    'Margem de Lucro Estimada': ['~10%', '~10%', '~20%', '~15-20%', '~10-15%', '~20-25%', '~10-15%', '~15-20%', '~20-25%', '~10-15%'],
    'Lucro Anual Estimado': ['~R$ 1,2 bilhões', '~R$ 300 milhões', '~R$ 2 bilhões', '~R$ 33 - 44 bilhões', '~R$ 60 - 90 bilhões', '~R$ 150 - 187,5 bilhões', '~R$ 50 - 75 bilhões', '~R$ 37,5 - 50 bilhões', '~R$ 1,2 - 1,5 trilhões', '~R$ 700 - 1.050 trilhões'],
    'Lucro Mensal Estimado': ['~R$ 100 milhões', '~R$ 25 milhões', '~R$ 166,7 milhões', '~R$ 2,75 - 3,67 bilhões', '~R$ 5 - 7,5 bilhões', '~R$ 12,5 - 15,6 bilhões', '~R$ 4,17 - 6,25 bilhões', '~R$ 3,125 - 4,17 bilhões', '~R$ 100 - 125 bilhões', '~R$ 58,3 - 87,5 bilhões'],
    'Lucro Diário Estimado': ['~R$ 3,3 milhões', '~R$ 833 mil', '~R$ 5,5 milhões', '~R$ 90 - 133 milhões', '~R$ 166 - 250 milhões', '~R$ 410 - 510 milhões', '~R$ 137 - 208 milhões', '~R$ 104 - 137 milhões', '~R$ 3,3 - 4,1 bilhões', '~R$ 1,9 - 2,4 bilhões'],
    '1% do Lucro Anual': ['~R$ 12 milhões', '~R$ 3 milhões', '~R$ 2 bilhões', '~R$ 33 - 44 bilhões', '~R$ 60 - 90 bilhões', '~R$ 150 - 187,5 bilhões', '~R$ 50 - 75 bilhões', '~R$ 37,5 - 50 bilhões', '~R$ 1,2 - 1,5 trilhões', '~R$ 700 - 1.050 trilhões'],
    '1% do Lucro Anual em 1 Mês': ['~R$ 1 milhão', '~R$ 250 mil', '~R$ 166,7 milhões', '~R$ 2,75 - 3,67 bilhões', '~R$ 5 - 7,5 bilhões', '~R$ 12,5 - 15,6 bilhões', '~R$ 4,17 - 6,25 bilhões', '~R$ 3,125 - 4,17 bilhões', '~R$ 100 - 125 bilhões', '~R$ 58,3 - 87,5 bilhões'],
    'Exemplos de Empresas': ['Havan', 'SBT, Sistema Brasileiro de Televisão', 'Airbnb', 'CrowdStrike, Palo Alto Networks', 'Google Ads, Meta Platforms', 'Salesforce, Microsoft Azure', 'Stripe, Square', 'Medtronic, Philips Healthcare', 'JPMorgan Chase, HSBC', 'Cargill, Bayer']
}

data_tabela_nacional = {
    'Mercado/Indivíduo': ['Luciano Hang', 'Silvio Santos', 'Airbnb', 'Cibersegurança', 'Marketing Digital', 'Tecnologia de SaaS', 'Fintechs', 'Tecnologia de Saúde', 'Banco', 'Agronegócio'],
    'Faturamento Anual Nacional Estimado': ['~R$ 12 bilhões', '~R$ 3 bilhões (SBT e outros)', '~R$ 1,5 bilhões (Brasil)', '~R$ 6 bilhões (Brasil)', '~R$ 40 bilhões (Brasil)', '~R$ 80 bilhões (Brasil)', '~R$ 30 bilhões (Brasil)', '~R$ 25 bilhões (Brasil)', '~R$ 800 bilhões (Brasil)', '~R$ 1 trilhão (Brasil)'],
    'Patrimônio Estimado': ['~R$ 2 bilhões', '~R$ 7 bilhões', '~R$ 15 bilhões', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', '~R$ 500 bilhões', 'N/A'],
    'Margem de Lucro Estimada': ['~10%', '~10%', '~15%', '~15%', '~10%', '~15%', '~10%', '~10%', '~20%', '~15%'],
    'Lucro Anual Estimado': ['~R$ 1,2 bilhões', '~R$ 300 milhões', '~R$ 225 milhões', '~R$ 900 milhões', '~R$ 4 bilhões', '~R$ 12 bilhões', '~R$ 3 bilhões', '~R$ 2,5 bilhões', '~R$ 160 bilhões', '~R$ 150 bilhões'],
    'Lucro Mensal Estimado': ['~R$ 100 milhões', '~R$ 25 milhões', '~R$ 18,75 milhões', '~R$ 75 milhões', '~R$ 333 milhões', '~R$ 1 bilhão', '~R$ 250 milhões', '~R$ 208 milhões', '~R$ 13,3 bilhões', '~R$ 12,5 bilhões'],
    'Lucro Diário Estimado': ['~R$ 3,3 milhões', '~R$ 833 mil', '~R$ 625 mil', '~R$ 2,5 milhões', '~R$ 11 milhões', '~R$ 33 milhões', '~R$ 8,3 milhões', '~R$ 6,9 milhões', '~R$ 440 milhões', '~R$ 415 milhões'],
    '1% do Lucro Anual': ['~R$ 12 milhões', '~R$ 3 milhões', '~R$ 2,25 bilhões', '~R$ 900 milhões', '~R$ 4 bilhões', '~R$ 12 bilhões', '~R$ 3 bilhões', '~R$ 2,5 bilhões', '~R$ 160 bilhões', '~R$ 150 bilhões'],
    '1% do Lucro Anual em 1 Mês': ['~R$ 1 milhão', '~R$ 250 mil', '~R$ 187,5 milhões', '~R$ 75 milhões', '~R$ 333 milhões', '~R$ 1 bilhão', '~R$ 250 milhões', '~R$ 208 milhões', '~R$ 13,3 bilhões', '~R$ 12,5 bilhões'],
    'Exemplos de Empresas': ['Havan', 'SBT, Sistema Brasileiro de Televisão', 'Airbnb', 'Tempest, Kaspersky', 'Nubank, GuiaBolso', 'Totvs, Linx', 'PagSeguro, Stone', 'Dasa, Hapvida', 'Itaú Unibanco, Bradesco', 'Cargill, JBS']
}

# Dados da nova tabela
data_tabela_investimento = {
    'Mercado/Indivíduo': ['Luciano Hang', 'Silvio Santos', 'Airbnb', 'Cibersegurança', 'Marketing Digital', 'Tecnologia de SaaS', 'Fintechs', 'Tecnologia de Saúde', 'Banco', 'Agronegócio'],
    'Número de Transações Global': ['~100 milhões', '~10 milhões', '~100 milhões', '~5 milhões', '~1 bilhão', '~50 milhões', '~2 bilhões', '~1 bilhão', '~3 bilhões', '~1,5 bilhões'],
    'Número de Transações Nacional': ['~60 milhões', '~5 milhões', '~10 milhões', '~500 mil', '~150 milhões', '~10 milhões', '~400 milhões', '~150 milhões', '~500 milhões', '~300 milhões'],
    'Tempo Médio para Estabilização Global': ['~5 anos', '~10 anos', '~5 anos', '~7 anos', '~3 anos', '~4 anos', '~4 anos', '~6 anos', '~20 anos', '~10 anos'],
    'Tempo Médio para Estabilização Nacional': ['~4 anos', '~8 anos', '~3 anos', '~5 anos', '~2 anos', '~3 anos', '~3 anos', '~5 anos', '~15 anos', '~8 anos'],
    'Investimento Médio para Começar em Cada Mercado do Zero': ['~R$ 50 milhões', '~R$ 20 milhões', '~R$ 100 milhões', '~R$ 30 milhões', '~R$ 200 milhões', '~R$ 80 milhões', '~R$ 150 milhões', '~R$ 100 milhões', '~R$ 500 milhões', '~R$ 300 milhões'],
    'Gasto Inicial no Primeiro Ano (Global)': ['~R$ 50 milhões', '~R$ 50 milhões', '~R$ 100 milhões', '~R$ 30 milhões', '~R$ 200 milhões', '~R$ 80 milhões', '~R$ 150 milhões', '~R$ 100 milhões', '~R$ 500 milhões', '~R$ 300 milhões'],
    'Gasto Inicial no Primeiro Ano (Nacional)': ['~R$ 20 milhões', '~R$ 10 milhões', '~R$ 50 milhões', '~R$ 10 milhões', '~R$ 80 milhões', '~R$ 30 milhões', '~R$ 60 milhões', '~R$ 40 milhões', '~R$ 200 milhões', '~R$ 120 milhões'],
    'Investimento Inicial para Iniciantes': ['~R$ 5 milhões', '~R$ 1 milhão', '~R$ 10 milhões', '~R$ 1 milhão', '~R$ 2 milhões', '~R$ 500 mil', '~R$ 2 milhões', '~R$ 1 milhão', '~R$ 10 milhões', '~R$ 5 milhões']
}

# Streamlit app
st.title('Análise de Dados de Mercado')

# Título na barra lateral
st.sidebar.title('VIRTUS GLOBAL')

# Filtro para selecionar a tabela
tabela_selecionada = st.sidebar.selectbox(
    'ESTUDO DE MERCADO: Selecione a Tabela',
    ['Tabela de Ticket Médio Global', 'Tabela de Ticket Médio Nacional', 'Tabela Global', 'Tabela Nacional', 'Tabela de Investimento']
)

# Filtro para selecionar as notas gerais
notas_selecionadas = st.sidebar.selectbox(
    'ESTUDO DE MERCADO: Notas Gerais',
    ['Não exibir notas', 'Exibir notas gerais']
)

# Mostrar a tabela selecionada
if tabela_selecionada == 'Tabela de Ticket Médio Global':
    st.subheader('Tabela de Ticket Médio Global')
    df_tabela = pd.DataFrame(data_tabela_ticket_medio)
    st.write(df_tabela)

elif tabela_selecionada == 'Tabela de Ticket Médio Nacional':
    st.subheader('Tabela de Ticket Médio Nacional')
    df_tabela = pd.DataFrame(data_tabela_ticket_medio_nacional)
    st.write(df_tabela)

elif tabela_selecionada == 'Tabela Global':
    st.subheader('Tabela Global')
    df_tabela = pd.DataFrame(data_tabela_global)
    st.write(df_tabela)

elif tabela_selecionada == 'Tabela Nacional':
    st.subheader('Tabela Nacional')
    df_tabela = pd.DataFrame(data_tabela_nacional)
    st.write(df_tabela)

elif tabela_selecionada == 'Tabela de Investimento':
    st.subheader('Tabela de Investimento')
    df_tabela = pd.DataFrame(data_tabela_investimento)
    st.write(df_tabela)

# Mostrar notas gerais se selecionado
if notas_selecionadas == 'Exibir notas gerais':
    st.subheader('Notas Gerais')
    st.markdown("""
    **Qual mercado tem o menor investimento para iniciantes?**
    Silvio Santos com um investimento inicial de R$ 1 milhão.

    **Qual mercado tem o menor número de transações?**
    Cibersegurança com 5 milhões de transações globais e 500 mil transações nacionais.

    **Qual mercado tem o maior número de transações?**
    Marketing Digital com 1 bilhão de transações globais e 150 milhões de transações nacionais.

    **Qual mercado tem o maior patrimônio estimado?**
    Banco com um patrimônio estimado global de R$ 2 trilhões.

    **Qual mercado tem a maior margem de lucro estimada?**
    Tecnologia de SaaS com uma margem de lucro estimada de 20-25%.

    **Qual mercado tem o maior lucro anual estimado?**
    Banco com um lucro anual estimado global de R$ 1,2 - 1,5 trilhões.

    **Qual mercado tem o maior lucro mensal estimado?**
    Banco com um lucro mensal estimado global de R$ 100 - 125 bilhões.

    **Qual mercado tem a menor margem de lucro?**
    Marketing Digital com uma margem de lucro estimada de 10-15%.

    **Qual mercado tem o menor patrimônio?**
    Tecnologia de Saúde com um patrimônio estimado globalmente de N/A (não disponível).

    **Qual mercado tem o menor lucro anual com 1% de participação?**
    Cibersegurança com um lucro anual de R$ 33 - 44 bilhões (global), representando 1% do lucro anual global.
    """)
