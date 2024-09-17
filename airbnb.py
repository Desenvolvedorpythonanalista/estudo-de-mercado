import streamlit as st
import pandas as pd
from io import BytesIO
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

# Função para calcular o valor da parcela do financiamento
def calcular_parcela(valor_imovel, entrada, taxa_juros, prazo_anos):
    valor_financiado = valor_imovel - entrada
    taxa_juros_mensal = taxa_juros / 12 / 100
    prazo_meses = prazo_anos * 12
    parcela = valor_financiado * taxa_juros_mensal * (1 + taxa_juros_mensal) ** prazo_meses / ((1 + taxa_juros_mensal) ** prazo_meses - 1)
    return parcela

# Função para calcular a receita mensal e lucro
def calcular_renda(valor_diaria, qtd_imoveis, dias_ocupacao, custos_fixos, taxa_administracao, percentual_lucro):
    receita_mensal_total = valor_diaria * qtd_imoveis * dias_ocupacao
    receita_após_administracao = receita_mensal_total * (1 - taxa_administracao / 100)
    receita_liquida = receita_após_administracao - custos_fixos
    receita_pessoal = receita_liquida * percentual_lucro / 100
    receita_gestor = receita_após_administracao - receita_pessoal
    lucro_mensal = receita_liquida
    return receita_mensal_total, receita_liquida, receita_pessoal, receita_gestor, lucro_mensal

# Função para calcular o tempo necessário para alcançar o valor da parcela
def tempo_para_alcancar(valor_parcela, valor_diaria, qtd_imoveis):
    receita_diaria_total = valor_diaria * qtd_imoveis
    tempo_dias = valor_parcela / receita_diaria_total
    return int(round(tempo_dias))

# Função para formatar valores com base na moeda selecionada
def formatar_valor(valor, moeda):
    if moeda == 'USD':
        return f'${valor:,.2f}'
    elif moeda == 'BRL':
        return f'R${valor:,.2f}'
    elif moeda == 'EUR':
        return f'€{valor:,.2f}'

# Função para gerar PDF
def gerar_pdf(tabelas):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    for titulo, tabela in tabelas:
        content.append(Paragraph(titulo, styles['Title']))
        
        # Criação da tabela
        data = [list(row) for row in tabela]
        table = Table(data, colWidths=[150, 150])
        
        # Estilo da tabela
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        content.append(table)
        content.append(Paragraph('', styles['Normal']))  # Espaço entre tabelas
    
    doc.build(content)
    buffer.seek(0)
    return buffer.read()

# Interface do Streamlit
st.title('Calculadora de Financiamento Imobiliário e Renda Airbnb')

# Barra lateral para seleção da moeda
moeda = st.sidebar.selectbox('Selecionar Moeda', ['USD', 'BRL', 'EUR'])

# Campos de entrada
valor_imovel = st.number_input('Valor do Imóvel', value=400000, step=1000)
entrada_percentual = st.slider('Entrada (%)', 0, 100, 10)
entrada = valor_imovel * entrada_percentual / 100
taxa_juros = st.number_input('Taxa de Juros Anual (%)', value=4.0, step=0.1)
prazo_anos = st.number_input('Prazo do Financiamento (anos)', value=30, step=1)
renda_desejada = st.number_input('Renda Desejada', value=6000, step=100)
valor_diaria = st.number_input('Diária por Imóvel', value=250, step=10)
custos_fixos = st.number_input('Custos Fixos Mensais', value=2000, step=100)
qtd_imoveis = st.number_input('Quantidade de Imóveis', value=1, step=1)
taxa_administracao = st.number_input('Taxa de Administração (%)', value=10.0, step=0.5)
percentual_lucro = st.number_input('Percentual de Lucro Pessoal (%)', value=30.0, step=1.0)
percentual_reinvestir = st.number_input('Percentual de Lucro Mensal para Reinvestir (%)', value=50.0, step=1.0)

# Campos adicionais
regras_casa = st.text_input('Regras da Casa', 'Anote aqui as regras da casa')
faixa_etaria = st.text_input('Faixa Etária Preferida', 'Anote aqui a faixa etária preferida')
melhores_meses = st.text_input('Melhores Meses', 'Anote aqui os melhores meses')
meses_sazonalidade = st.text_input('Meses de Sazonalidade', 'Anote aqui os meses de sazonalidade')

# Botão para calcular
if st.button('Calcular'):
    # Cálculos
    valor_parcela = calcular_parcela(valor_imovel, entrada, taxa_juros, prazo_anos)
    receita_mensal_total, receita_liquida, receita_pessoal, receita_gestor, lucro_mensal = calcular_renda(
        valor_diaria, qtd_imoveis, 30, custos_fixos, taxa_administracao, percentual_lucro
    )
    tempo_dias = tempo_para_alcancar(valor_parcela, valor_diaria, qtd_imoveis)
    
    # Cálculo do reinvestimento
    valor_reinvestir = lucro_mensal * percentual_reinvestir / 100
    lucro_nao_distribuido = lucro_mensal - valor_reinvestir

    # Tabelas
    tabelas = [
        ('Tabela de Financiamento Imobiliário', [
            ['Valor do Imóvel', formatar_valor(valor_imovel, moeda)],
            ['Entrada', formatar_valor(entrada, moeda)],
            ['Valor Financiado', formatar_valor(valor_imovel - entrada, moeda)],
            ['Prazo do Financiamento', f'{prazo_anos} anos'],
            ['Taxa de Juros Anual', f'{taxa_juros}%'],
            ['Valor da Parcela (aprox.)', formatar_valor(valor_parcela, moeda)],
            ['Valor da Parcela em 10 anos (aprox.)', formatar_valor(calcular_parcela(valor_imovel, entrada, taxa_juros, 10), moeda)],
            ['Valor da Parcela em 5 anos (aprox.)', formatar_valor(calcular_parcela(valor_imovel, entrada, taxa_juros, 5), moeda)]
        ]),
        ('Tabela de Renda Airbnb', [
            ['Renda Desejada', formatar_valor(renda_desejada, moeda)],
            ['Diária por Imóvel', formatar_valor(valor_diaria, moeda)],
            ['Receita Mensal Total (1 imóvel)', formatar_valor(receita_mensal_total, moeda)]
        ]),
        ('Tempo para Alcançar o Valor da Parcela', [
            ['Período de Amortização', '30 anos'],
            ['Valor da Parcela', formatar_valor(valor_parcela, moeda)],
            ['Tempo para Alcançar o Valor da Parcela (dias)', tempo_dias]
        ]),
        ('Receita Líquida e Lucro Após Custos', [
            ['Receita Mensal Total', formatar_valor(receita_mensal_total, moeda)],
            ['Percentual de Receita Líquida', f'{percentual_lucro}%'],
            ['Custos Fixos Mensais', formatar_valor(custos_fixos, moeda)],
            ['Custos Pessoais Mensais', formatar_valor(custos_fixos * 1.5, moeda)],
            ['Total de Custos Mensais', formatar_valor(custos_fixos * 2.5, moeda)],
            ['Lucro Mensal (Após Custos)', formatar_valor(lucro_mensal, moeda)]
        ]),
        ('Reinvestimento Baseado no Lucro Mensal Após Custos', [
            ['Lucro Mensal (Após Custos)', formatar_valor(lucro_mensal, moeda)],
            ['Percentual para Reinvestir', f'{percentual_reinvestir}%'],
            ['Valor a Reinvestir', formatar_valor(valor_reinvestir, moeda)],
            ['Lucro Não Distribuído', formatar_valor(lucro_nao_distribuido, moeda)]
        ]),
        ('Dados Airbnb com Estadia Mínima de 3 Dias', [
            ['Regras da Casa', regras_casa],
            ['Faixa Etária Preferida', faixa_etaria],
            ['Melhores Meses', melhores_meses],
            ['Meses de Sazonalidade', meses_sazonalidade]
        ])
    ]

    # Gerar e exibir o PDF
    pdf_output = gerar_pdf(tabelas)

    st.download_button(
        label="Baixar Relatório em PDF",
        data=pdf_output,
        file_name="relatorio_airbnb.pdf",
        mime="application/pdf"
    )

    # Mostrar Tabelas na Interface
    for titulo, tabela in tabelas:
        df = pd.DataFrame(tabela, columns=['Descrição', 'Valores'])
        st.write(f"### {titulo}")
        st.dataframe(df)
