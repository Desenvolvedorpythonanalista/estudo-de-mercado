import pandas as pd
import streamlit as st

def calcular_valores(investimento_desejado, distribuicao_lucro, custos_fixos_mensais, margem_lucro, valor_por_venda, taxa_cambio, moeda):
    # Função para converter valores
    def converter_para_moeda(valor, moeda):
        if moeda == "BRL":
            return valor * taxa_cambio
        else:
            return valor

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
    
    if valor_por_venda > 0:
        numero_vendas_com_30_comissao_mes = custo_fixo_mensal / (valor_por_venda * 0.30)
    else:
        numero_vendas_com_30_comissao_mes = 0

    rentabilidade_mensal_investidores = (distribuicao_lucro_investidor * faturamento_necessario_mensal) / investimento_desejado
    rentabilidade_mensal_fundador = (distribuicao_lucro_fundador * faturamento_necessario_mensal) / investimento_desejado

    return {
        "Investimento Desejado": f"{converter_para_moeda(investimento_desejado, moeda):,.2f} {moeda}",
        "Distribuição de Lucro para o Investidor": f"{distribuicao_lucro * 100:.2f}%",
        "Custos Fixos (Mês)": f"{converter_para_moeda(custos_fixos_mensais, moeda):,.2f} {moeda}",
        "Custos Fixos (Ano)": f"{converter_para_moeda(custos_fixos_mensais * 12, moeda):,.2f} {moeda}",
        "Margem de Lucro": f"{margem_lucro * 100:.2f}%",
        "Faturamento Anual Previsto": f"{converter_para_moeda(faturamento_necessario_anual, moeda):,.2f} {moeda}",
        "Faturamento Mensal Previsto": f"{converter_para_moeda(faturamento_necessario_mensal, moeda):,.2f} {moeda}",
        "Número de Vendas com 100% de Comissão (Ano)": f"{int(numero_vendas_com_100_comissao_ano)} produtos ou clientes",
        "Número de Vendas com 30% de Comissão (Mês)": f"{int(numero_vendas_com_30_comissao_mes)} produtos ou clientes",
        "Valor de Administração (30%)": f"{converter_para_moeda(faturamento_necessario_mensal * 0.30, moeda):,.2f} {moeda}",
        "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
        "Meta do Mês para Bater o Faturamento Mensal Médio": f"{converter_para_moeda(faturamento_necessario_mensal, moeda):,.2f} {moeda}",
        "Valor para Investidores (anual)": f"{converter_para_moeda(faturamento_necessario_anual * distribuicao_lucro_investidor, moeda):,.2f} {moeda}",
        "Valor para Investidores (mensal)": f"{converter_para_moeda(faturamento_necessario_mensal * distribuicao_lucro_investidor, moeda):,.2f} {moeda}",
        "Distribuição de Lucro para Sócio Fundador": f"{distribuicao_lucro_fundador * 100:.2f}%",
        "Valor para Sócio Fundador (anual)": f"{converter_para_moeda(valor_fundador_anual, moeda):,.2f} {moeda}",
        "Valor para Sócio Fundador (mensal)": f"{converter_para_moeda(valor_fundador_mensal, moeda):,.2f} {moeda}",
        "Notas": (
            f"Valor para Sócio Fundador (anual): {converter_para_moeda(valor_fundador_anual, moeda):,.2f} {moeda}\n"
            f"Valor para Sócio Fundador (mensal): {converter_para_moeda(valor_fundador_mensal, moeda):,.2f} {moeda}"
        ),
        "Rentabilidade Mensal (Investidores)": f"{rentabilidade_mensal_investidores * 100:.2f}%",
        "Rentabilidade Mensal (Sócio Fundador)": f"{rentabilidade_mensal_fundador * 100:.2f}%",
        "Valor por Venda/Assinatura": f"{converter_para_moeda(valor_por_venda, moeda):,.2f} {moeda}"
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
            "Número de Vendas com 100% de Comissão (Ano)": "120 produtos",
            "Número de Vendas com 30% de Comissão (Mês)": "10 produtos",
            "Valor de Administração (30%)": "29.647,06 USD",
            "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
            "Meta do Mês para Bater o Faturamento Mensal Médio": "98.823,53 USD",
            "Valor para Investidores (anual)": "300.000,00 USD",
            "Valor para Investidores (mensal)": "25.000,00 USD",
            "Distribuição de Lucro para Sócio Fundador": "70%",
            "Valor para Sócio Fundador (anual)": "840.000,00 USD",
            "Valor para Sócio Fundador (mensal)": "70.000,00 USD",
            "Notas": (
                "Valor para Sócio Fundador (anual): 4.200.000 BRL\n"
                "Valor para Sócio Fundador (mensal): 350.000 BRL"
            ),
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
            "Número de Vendas com 100% de Comissão (Ano)": "1.200 produtos",
            "Número de Vendas com 30% de Comissão (Mês)": "100 produtos",
            "Valor de Administração (30%)": "294.117,65 USD",
            "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
            "Meta do Mês para Bater o Faturamento Mensal Médio": "980.392,86 USD",
            "Valor para Investidores (anual)": "300.000,00 USD",
            "Valor para Investidores (mensal)": "25.000,00 USD",
            "Distribuição de Lucro para Sócio Fundador": "70%",
            "Valor para Sócio Fundador (anual)": "8.400.000,00 USD",
            "Valor para Sócio Fundador (mensal)": "700.000,00 USD",
            "Notas": (
                "Valor para Sócio Fundador (anual): 42.000.000 BRL\n"
                "Valor para Sócio Fundador (mensal): 3.500.000 BRL"
            ),
            "Rentabilidade Mensal (Investidores)": "30,00%",
            "Rentabilidade Mensal (Sócio Fundador)": "70,00%"
        },
        2040: {
            "Investimento Desejado": "1.000.000 USD",
            "Distribuição de Lucro para o Investidor": "30%",
            "Custos Fixos (Mês)": "490.196,08 USD",
            "Custos Fixos (Ano)": "5.882.352,94 USD",
            "Margem de Lucro": "50%",
            "Faturamento Anual Previsto": "11.764.705,88 USD",
            "Faturamento Mensal Previsto": "980.392,86 USD",
            "Número de Vendas com 100% de Comissão (Ano)": "1.200 produtos",
            "Número de Vendas com 30% de Comissão (Mês)": "100 produtos",
            "Valor de Administração (30%)": "294.117,65 USD",
            "Tempo para Recuperar Investimento Inicial (cada sócio)": "Aproximadamente 7,5 meses",
            "Meta do Mês para Bater o Faturamento Mensal Médio": "980.392,86 USD",
            "Valor para Investidores (anual)": "300.000,00 USD",
            "Valor para Investidores (mensal)": "25.000,00 USD",
            "Distribuição de Lucro para Sócio Fundador": "70%",
            "Valor para Sócio Fundador (anual)": "8.400.000,00 USD",
            "Valor para Sócio Fundador (mensal)": "700.000,00 USD",
            "Notas": (
                "Valor para Sócio Fundador (anual): 42.000.000 BRL\n"
                "Valor para Sócio Fundador (mensal): 3.500.000 BRL"
            ),
            "Rentabilidade Mensal (Investidores)": "30,00%",
            "Rentabilidade Mensal (Sócio Fundador)": "70,00%"
        }
    }

    return dados

def main():
    st.title("Calculadora de Rentabilidade e Vendas")

    # Inputs
    investimento_desejado = st.number_input("Investimento Desejado (USD)", value=1000000.00)
    distribuicao_lucro = st.slider("Distribuição de Lucro para o Investidor", min_value=0.0, max_value=1.0, value=0.30, step=0.01)
    custos_fixos_mensais = st.number_input("Custos Fixos Mensais (USD)", value=49019.61)
    margem_lucro = st.slider("Margem de Lucro", min_value=0.0, max_value=1.0, value=0.50, step=0.01)
    valor_por_venda = st.number_input("Valor por Venda/Assinatura (USD)", value=5000.00)
    quantidade_produtos = st.number_input("Quantidade de Produtos ou Clientes", value=16, min_value=1)

    # Barra lateral para moeda
    moeda = st.sidebar.selectbox("Escolha a Moeda", options=["USD", "BRL"])

    # Taxa de Câmbio opcional na barra lateral
    taxa_cambio = st.sidebar.number_input("Taxa de Câmbio (USD para BRL)", value=5.00, format="%f")

    # Botão para calcular
    if st.button("Calcular"):
        # Cálculos
        resultados = calcular_valores(
            investimento_desejado, distribuicao_lucro, custos_fixos_mensais, margem_lucro,
            valor_por_venda, taxa_cambio, moeda
        )

        # Exibir resultados
        st.write("### Resultados Calculados")
        for chave, valor in resultados.items():
            st.write(f"**{chave}:** {valor}")

    # Barra lateral para dados estáticos
    st.sidebar.header('Dados Estáticos')
    mostrar_dados_estaticos = st.sidebar.checkbox('Mostrar Dados Estáticos', value=True)

    if mostrar_dados_estaticos:
        dados = atualizar_tabelas()

        # Filtro de ano
        ano_selecionado = st.sidebar.selectbox("Escolha o Ano", options=[2030, 2035, 2040])

        st.sidebar.write("### Dados do Ano Selecionado")
        st.sidebar.write(pd.DataFrame(dados[ano_selecionado].items(), columns=['Campo', 'Valor']).set_index('Campo'))

        st.write("### Dados Estáticos")
        st.write(pd.DataFrame(dados[ano_selecionado].items(), columns=['Campo', 'Valor']).set_index('Campo'))

if __name__ == "__main__":
    main()
