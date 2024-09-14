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
        numero_vendas_com_100_comissao_ano = custo_fixo_anual / faturamento_necessario_anual
    else:
        numero_vendas_com_100_comissao_ano = 0
    
    if faturamento_necessario_mensal > 0:
        numero_vendas_com_30_comissao_mes = custo_fixo_mensal / (faturamento_necessario_mensal * 0.30)
    else:
        numero_vendas_com_30_comissao_mes = 0

    rentabilidade_mensal_investidores = (distribuicao_lucro_investidor * faturamento_necessario_mensal) / investimento_desejado
    rentabilidade_mensal_fundador = (distribuicao_lucro_fundador * faturamento_necessario_mensal) / investimento_desejado

    valor_por_venda = faturamento_necessario_mensal / (numero_vendas_com_30_comissao_mes if numero_vendas_com_30_comissao_mes > 0 else 1)

    return {
        "Investimento Desejado": f"{investimento_desejado:,.2f} USD",
        "Distribuição de Lucro para o Investidor": f"{distribuicao_lucro * 100:.2f}%",
        "Custos Fixos (Mês)": f"{custos_fixos_mensais:,.2f} USD",
        "Custos Fixos (Ano)": f"{custos_fixos_mensais * 12:,.2f} USD",
        "Margem de Lucro": f"{margem_lucro * 100:.2f}%",
        "Faturamento Anual Previsto": f"{faturamento_necessario_anual:,.2f} USD",
        "Faturamento Mensal Previsto": f"{faturamento_necessario_mensal:,.2f} USD",
        "Número de Vendas com 100% de Comissão (Ano)": f"{int(numero_vendas_com_100_comissao_ano)} imóveis ou clientes",
        "Número de Vendas com 30% de Comissão (Mês)": f"{int(numero_vendas_com_30_comissao_mes)} imóveis ou clientes",
        "Valor de Administração (30%)": f"{faturamento_necessario_mensal * 0.30:,.2f} USD",
        "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
        "Meta do Mês para Bater o Faturamento Mensal Médio": f"{faturamento_necessario_mensal:,.2f} USD",
        "Valor para Investidores (anual)": f"{faturamento_necessario_anual * distribuicao_lucro_investidor:,.2f} USD",
        "Valor para Investidores (mensal)": f"{faturamento_necessario_mensal * distribuicao_lucro_investidor:,.2f} USD",
        "Distribuição de Lucro para Sócio Fundador": f"{distribuicao_lucro_fundador * 100:.2f}%",
        "Valor para Sócio Fundador (anual)": f"{valor_fundador_anual:,.2f} USD",
        "Valor para Sócio Fundador (mensal)": f"{valor_fundador_mensal:,.2f} USD",
        "Notas": f"Valor para Sócio Fundador (anual): {valor_fundador_anual * 5:,.2f} BRL\nValor para Sócio Fundador (mensal): {valor_fundador_mensal * 5:,.2f} BRL",
        "Rentabilidade Mensal (Investidores)": f"{rentabilidade_mensal_investidores * 100:.2f}%",
        "Rentabilidade Mensal (Sócio Fundador)": f"{rentabilidade_mensal_fundador * 100:.2f}%",
        "Valor por Venda/Assinatura": f"{valor_por_venda:,.2f} USD"
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
            "Número de Vendas com 100% de Comissão (Ano)": "120 imóveis",
            "Número de Vendas com 30% de Comissão (Mês)": "10 imóveis",
            "Valor de Administração (30%)": "29.647,06 USD",
            "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
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
            "Número de Vendas com 100% de Comissão (Ano)": "1.200 imóveis",
            "Número de Vendas com 30% de Comissão (Mês)": "100 imóveis",
            "Valor de Administração (30%)": "294.117,65 USD",
            "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
            "Meta do Mês para Bater o Faturamento Mensal Médio": "980.392,86 USD",
            "Valor para Investidores (anual)": "300.000,00 USD",
            "Valor para Investidores (mensal)": "25.000,00 USD",
            "Distribuição de Lucro para Sócio Fundador": "70%",
            "Valor para Sócio Fundador (anual)": "8.400.000,00 USD",
            "Valor para Sócio Fundador (mensal)": "700.000,00 USD",
            "Notas": "Valor para Sócio Fundador (anual): 42.000.000 BRL\nValor para Sócio Fundador (mensal): 3.500.000 BRL",
            "Rentabilidade Mensal (Investidores)": "30,00%",
            "Rentabilidade Mensal (Sócio Fundador)": "70,00%"
        }
    }
    
    return dados

# Streamlit Interface
st.title("Calculadora de Rentabilidade e Vendas")

# Inputs
investimento_desejado = st.number_input("Investimento Desejado (USD)", value=1000000.00)
distribuicao_lucro = st.slider("Distribuição de Lucro para o Investidor", min_value=0.0, max_value=1.0, value=0.30, step=0.01)
custos_fixos_mensais = st.number_input("Custos Fixos Mensais (USD)", value=49019.61)
margem_lucro = st.slider("Margem de Lucro", min_value=0.0, max_value=1.0, value=0.50, step=0.01)

# Calculations
resultados = calcular_valores(investimento_desejado, distribuicao_lucro, custos_fixos_mensais, margem_lucro)

# Display results
st.write("### Resultados Calculados")
for chave, valor in resultados.items():
    st.write(f"**{chave}:** {valor}")

# Display static data for 2030 and 2035
dados = atualizar_tabelas()
st.write("### Dados Estáticos")
for ano, info in dados.items():
    st.write(f"#### Ano {ano}")
    for chave, valor in info.items():
        st.write(f"**{chave}:** {valor}")
