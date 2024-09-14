import pandas as pd
import streamlit as st

def calcular_valores(investimento_desejado, distribuicao_lucro, custos_fixos_mensais, margem_lucro):
    valor_fundador_mensal = investimento_desejado * (1 - distribuicao_lucro)
    valor_fundador_anual = valor_fundador_mensal * 12
    distribuicao_lucro_investidor = distribuicao_lucro
    distribuicao_lucro_fundador = 1 - distribuicao_lucro

    # Cálculo do faturamento necessário para cobrir os custos e garantir lucro desejado
    faturamento_necessario_anual = valor_fundador_anual / distribuicao_lucro_fundador
    faturamento_necessario_mensal = faturamento_necessario_anual / 12
    
    custo_fixo_anual = custos_fixos_mensais * 12
    custo_fixo_mensal = custos_fixos_mensais
    
    if faturamento_necessario_anual > 0:
        numero_vendas_necessarias_ano = custo_fixo_anual / (faturamento_necessario_anual / 12)
    else:
        numero_vendas_necessarias_ano = 0
    
    if faturamento_necessario_mensal > 0:
        numero_vendas_necessarias_mes = custo_fixo_mensal / (faturamento_necessario_mensal / 12)
    else:
        numero_vendas_necessarias_mes = 0
    
    rentabilidade_mensal_investidores = (distribuicao_lucro_investidor * faturamento_necessario_mensal) / investimento_desejado
    rentabilidade_mensal_fundador = (distribuicao_lucro_fundador * faturamento_necessario_mensal) / investimento_desejado
    
    return {
        "Investimento Desejado": f"{investimento_desejado:,.2f} USD",
        "Distribuição de Lucro para o Investidor": f"{distribuicao_lucro * 100:.2f}%",
        "Custos Fixos (Mês)": f"{custos_fixos_mensais:,.2f} USD",
        "Custos Fixos (Ano)": f"{custos_fixos_mensais * 12:,.2f} USD",
        "Margem de Lucro": f"{margem_lucro * 100:.2f}%",
        "Faturamento Anual Previsto": f"{faturamento_necessario_anual:,.2f} USD",
        "Faturamento Mensal Previsto": f"{faturamento_necessario_mensal:,.2f} USD",
        "Número de Vendas Necessárias para Cobrir Custos Fixos (Ano)": f"{int(numero_vendas_necessarias_ano)} imóveis ou clientes",
        "Número de Vendas Necessárias para Cobrir Custos Fixos (Mês)": f"{int(numero_vendas_necessarias_mes)} imóveis ou clientes",
        "Valor de Administração (30%)": f"{faturamento_necessario_mensal * 0.30:,.2f} USD",
        "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
        "Faturamento Médio Anual para Garantir Lucro Mínimo de 100K dólares para o Investidor (Ano)": f"{faturamento_necessario_anual:,.2f} USD",
        "Faturamento Médio Mensal para Garantir Lucro Mínimo de 100K dólares para o Investidor (Mês)": f"{faturamento_necessario_mensal:,.2f} USD",
        "Meta do Mês para Bater o Faturamento Mensal Médio": f"{faturamento_necessario_mensal:,.2f} USD",
        "Valor para Investidores (anual)": f"{faturamento_necessario_anual * distribuicao_lucro_investidor:,.2f} USD",
        "Valor para Investidores (mensal)": f"{faturamento_necessario_mensal * distribuicao_lucro_investidor:,.2f} USD",
        "Distribuição de Lucro para Sócio Fundador": f"{distribuicao_lucro_fundador * 100:.2f}%",
        "Valor para Sócio Fundador (anual)": f"{valor_fundador_anual:,.2f} USD",
        "Valor para Sócio Fundador (mensal)": f"{valor_fundador_mensal:,.2f} USD",
        "Notas": f"Valor para Sócio Fundador (anual): {valor_fundador_anual * 5:,.2f} BRL\nValor para Sócio Fundador (mensal): {valor_fundador_mensal * 5:,.2f} BRL",
        "Rentabilidade Mensal (Investidores)": f"{rentabilidade_mensal_investidores * 100:.2f}%",
        "Rentabilidade Mensal (Sócio Fundador)": f"{rentabilidade_mensal_fundador * 100:.2f}%"
    }

def atualizar_tabelas():
    # Dados fixos para cada ano
    dados = {
        2030: {
            "Investimento Desejado": "1.000.000 USD",
            "Distribuição de Lucro para o Investidor": "30%",
            "Custos Fixos (Mês)": "49.019,61 USD",
            "Custos Fixos (Ano)": "588.235,29 USD",
            "Margem de Lucro": "50%",
            "Faturamento Anual Previsto": "1.176.470,59 USD",
            "Faturamento Mensal Previsto": "98.823,53 USD",
            "Número de Vendas Necessárias para Cobrir Custos Fixos (Ano)": "120 imóveis",
            "Número de Vendas Necessárias para Cobrir Custos Fixos (Mês)": "10 imóveis",
            "Valor de Administração (30%)": "29.647,06 USD",
            "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
            "Faturamento Médio Anual para Garantir Lucro Mínimo de 100K dólares para o Investidor (Ano)": "700.000 USD",
            "Faturamento Médio Mensal para Garantir Lucro Mínimo de 100K dólares para o Investidor (Mês)": "58.333,33 USD",
            "Meta do Mês para Bater o Faturamento Mensal Médio": "98.823,53 USD",
            "Valor para Investidores (anual)": "300.000,00 USD",
            "Valor para Investidores (mensal)": "25.000,00 USD",
            "Distribuição de Lucro para Sócio Fundador": "70%",
            "Valor para Sócio Fundador (anual)": "840.000,00 USD",
            "Valor para Sócio Fundador (mensal)": "70.000,00 USD",
            "Notas": "Valor para Sócio Fundador (anual): 4.200.000 BRL\nValor para Sócio Fundador (mensal): 350.000 BRL",
            "Rentabilidade Mensal (Investidores)": "30,00%",
            "Rentabilidade Mensal (Sócio Fundador)": "70,00%"
        },
        2035: {
            "Investimento Desejado": "1.000.000 USD",
            "Distribuição de Lucro para o Investidor": "30%",
            "Custos Fixos (Mês)": "490.196,08 USD",
            "Custos Fixos (Ano)": "5.882.352,94 USD",
            "Margem de Lucro": "50%",
            "Faturamento Anual Previsto": "11.764.705,88 USD",
            "Faturamento Mensal Previsto": "980.392,86 USD",
            "Número de Vendas Necessárias para Cobrir Custos Fixos (Ano)": "1.200 imóveis",
            "Número de Vendas Necessárias para Cobrir Custos Fixos (Mês)": "100 imóveis",
            "Valor de Administração (30%)": "294.117,65 USD",
            "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
            "Faturamento Médio Anual para Garantir Lucro Mínimo de 100K dólares para o Investidor (Ano)": "7.000.000 USD",
            "Faturamento Médio Mensal para Garantir Lucro Mínimo de 100K dólares para o Investidor (Mês)": "583.333,33 USD",
            "Meta do Mês para Bater o Faturamento Mensal Médio": "980.392,86 USD",
            "Valor para Investidores (anual)": "300.000,00 USD",
            "Valor para Investidores (mensal)": "25.000,00 USD",
            "Distribuição de Lucro para Sócio Fundador": "70%",
            "Valor para Sócio Fundador (anual)": "8.400.000,00 USD",
            "Valor para Sócio Fundador (mensal)": "700.000,00 USD",
            "Notas": "Valor para Sócio Fundador (anual): 42.000.000 BRL\nValor para Sócio Fundador (mensal): 3.500.000 BRL",
            "Rentabilidade Mensal (Investidores)": "30,00%",
            "Rentabilidade Mensal (Sócio Fundador)": "70,00%"
        },
        2040: {
            "Investimento Desejado": "10.000.000 USD",
            "Distribuição de Lucro para o Investidor": "30%",
            "Custos Fixos (Mês)": "4.901.960,78 USD",
            "Custos Fixos (Ano)": "58.823.529,41 USD",
            "Margem de Lucro": "50%",
            "Faturamento Anual Previsto": "117.647.058,82 USD",
            "Faturamento Mensal Previsto": "9.803.921,57 USD",
            "Número de Vendas Necessárias para Cobrir Custos Fixos (Ano)": "12.000 imóveis",
            "Número de Vendas Necessárias para Cobrir Custos Fixos (Mês)": "1.000 imóveis",
            "Valor de Administração (30%)": "2.941.176,47 USD",
            "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
            "Faturamento Médio Anual para Garantir Lucro Mínimo de 100K dólares para o Investidor (Ano)": "70.000.000 USD",
            "Faturamento Médio Mensal para Garantir Lucro Mínimo de 100K dólares para o Investidor (Mês)": "5.833.333,33 USD",
            "Meta do Mês para Bater o Faturamento Mensal Médio": "9.803.921,57 USD",
            "Valor para Investidores (anual)": "3.000.000,00 USD",
            "Valor para Investidores (mensal)": "250.000,00 USD",
            "Distribuição de Lucro para Sócio Fundador": "70%",
            "Valor para Sócio Fundador (anual)": "84.000.000,00 USD",
            "Valor para Sócio Fundador (mensal)": "7.000.000,00 USD",
            "Notas": "Valor para Sócio Fundador (anual): 420.000.000 BRL\nValor para Sócio Fundador (mensal): 35.000.000 BRL",
            "Rentabilidade Mensal (Investidores)": "30,00%",
            "Rentabilidade Mensal (Sócio Fundador)": "70,00%"
        }
    }
    
    return dados

def main():
    st.title('Análise Financeira da Empresa')

    # Atualiza as tabelas com valores fixos
    tabelas = atualizar_tabelas()

    st.sidebar.header('Configurações')
    investimento_desejado = st.sidebar.number_input("Investimento Desejado (USD)", min_value=0.0, format="%f")
    distribuicao_lucro = st.sidebar.slider("Distribuição de Lucro (%)", min_value=0, max_value=100, value=30) / 100.0
    custos_fixos_mensais = st.sidebar.number_input("Custos Fixos (Mensal) em USD", min_value=0.0, format="%f")
    margem_lucro = st.sidebar.slider("Margem de Lucro (%)", min_value=0, max_value=100, value=50) / 100.0

    # Exibir as tabelas para os anos de interesse
    periodos = {
        "Em 5 anos": 2030,
        "Em 10 anos": 2035,
        "Em 20 anos": 2040
    }

    for periodo, ano in periodos.items():
        dados = tabelas[ano]
        st.subheader(f'Dados da Empresa Previstos para {periodo}')
        st.write(pd.DataFrame(dados.items(), columns=['Campo', 'Valor']).set_index('Campo'))

    if st.button('Calcular Resultados'):
        dados_calculados = calcular_valores(investimento_desejado, distribuicao_lucro, custos_fixos_mensais, margem_lucro)
        st.subheader('Dados Calculados Baseado no Valor Desejado:')
        st.write(pd.DataFrame(dados_calculados.items(), columns=['Campo', 'Valor']).set_index('Campo'))

if __name__ == "__main__":
    main()
