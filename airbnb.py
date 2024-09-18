import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

# Função para calcular o valor da parcela do financiamento
def calcular_parcela(valor_imovel, entrada, taxa_juros, prazo_anos):
    valor_financiado = valor_imovel - entrada
    taxa_juros_mensal = taxa_juros / 12 / 100
    prazo_meses = prazo_anos * 12
    parcela = valor_financiado * taxa_juros_mensal * (1 + taxa_juros_mensal) ** prazo_meses / ((1 + taxa_juros_mensal) ** prazo_meses - 1)
    return parcela

# Função para calcular a receita mensal e lucro
def calcular_renda(valor_diaria, qtd_imoveis, dias_ocupacao, custos_fixos, taxa_administracao, valor_reserva_emergencia):
    receita_mensal_total = valor_diaria * qtd_imoveis * dias_ocupacao
    custo_administracao = receita_mensal_total * (taxa_administracao / 100)
    reserva_emergencia = valor_reserva_emergencia
    total_custos_mensais = custos_fixos + calcular_parcela(valor_imovel, entrada, taxa_juros, prazo_anos) + custo_administracao + reserva_emergencia
    lucro_mensal = receita_mensal_total - total_custos_mensais
    return receita_mensal_total, custo_administracao, reserva_emergencia, total_custos_mensais, lucro_mensal

# Função para calcular o tempo necessário para alcançar o valor da parcela
def tempo_para_alcancar(valor_parcela, valor_diaria, qtd_imoveis):
    receita_diaria_total = valor_diaria * qtd_imoveis
    tempo_dias = valor_parcela / receita_diaria_total
    return int(-(-tempo_dias // 1))  # Arredondar sempre para cima

# Função para calcular o valor total pago ao final do financiamento
def calcular_valor_total_pago(valor_parcela, prazo_anos):
    prazo_meses = prazo_anos * 12
    return valor_parcela * prazo_meses

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
st.title('Virtus Life Global LLC. Investimentos')

# Introdução e Instruções
st.write("""
### Bem-vindo ou Bem-vinda à nossa Simulação de Investimentos Imobiliários e Renda com Aluguéis!

Esta ferramenta ajuda você a avaliar a viabilidade financeira do seu investimento imobiliário, calculando parcelas de financiamento e potencial de lucro com aluguel de curto prazo (como no Airbnb). 

#### Como Usar:
1. **Preencha os campos abaixo** com as informações do seu imóvel e financiamento.
2. **Clique em "Calcular"** para ver os resultados.

#### Campos de Entrada:
- **Valor do Imóvel**: Indique o valor total do imóvel que você pretende financiar.
- **Entrada (%)**: Informe o percentual do valor do imóvel que será pago como entrada.
- **Taxa de Juros Anual (%)**: Forneça a taxa de juros anual do financiamento.
- **Prazo do Financiamento (anos)**: Defina o número de anos para quitar o financiamento.
- **Renda Desejada**: Determine a renda mensal que você deseja obter com o aluguel.
- **Diária por Imóvel**: Especifique o valor que será cobrado por dia de aluguel.
- **Custos Fixos Mensais**: Informe as despesas fixas mensais que você terá.
- **Quantidade de Imóveis**: Informe o número de imóveis que você pretende alugar.
- **Taxa de Administração (%)**: Indique o percentual da receita mensal que será gasto com administração.
- **Valor para Reserva de Emergência**: Determine a quantia destinada a cobrir emergências.
- **Percentual de Lucro Mensal para Reinvestir (%)**: Defina o percentual do lucro mensal que você planeja reinvestir.

#### Resultados
Após preencher os campos e clicar em "Calcular", a ferramenta gerará os seguintes resultados:
- **Tabelas de Financiamento Imobiliário**: Informações detalhadas sobre o seu financiamento.
- **Tabela de Renda Airbnb**: Cálculos da renda mensal baseada nas diárias e ocupação.
- **Tempo para Alcançar o Valor da Parcela**: Quanto tempo você precisará para gerar receita suficiente para cobrir a parcela do financiamento.
- **Receita Líquida e Lucro Após Custos**: Visão geral dos custos e lucros.
- **Reinvestimento Baseado no Lucro Mensal Após Custos**: Quanto você pode reinvestir e quanto lucro você manterá.

Você pode recalcular quantas vezes quiser, ajustando os valores conforme necessário. Se precisar de ajuda, estamos à disposição! Se tiver qualquer dúvida ou sugestão, pode enviar uma mensagem para o meu WhatsApp: (91) 99942-5135.
""")

# Barra lateral para seleção da moeda
moeda = st.sidebar.selectbox('Selecionar Moeda', ['USD', 'BRL', 'EUR'])

# Campos de entrada
valor_imovel = st.number_input('Valor do Imóvel', value=None, step=1000)
entrada_percentual = st.slider('Entrada (%)', 0, 100, 0)
entrada = valor_imovel * entrada_percentual / 100 if valor_imovel is not None else 0
taxa_juros = st.number_input('Taxa de Juros Anual (%)', value=None, step=0.1)
prazo_anos = st.number_input('Prazo do Financiamento (anos)', value=None, step=1)
renda_desejada = st.number_input('Renda Desejada', value=None, step=100)
valor_diaria = st.number_input('Diária por Imóvel', value=None, step=10)
custos_fixos = st.number_input('Custos Fixos Mensais', value=None, step=100)
qtd_imoveis = st.number_input('Quantidade de Imóveis', value=None, step=1)
taxa_administracao = st.number_input('Taxa de Administração (%)', value=None, step=0.5)
valor_reserva_emergencia = st.number_input('Valor para Reserva de Emergência', value=None, step=100)
percentual_reinvestir = st.number_input('Percentual de Lucro Mensal para Reinvestir (%)', value=None, step=1.0)

# Campos adicionais
regras_casa = st.text_input('Regras da Casa', '')
faixa_etaria = st.text_input('Faixa Etária Preferida', '')
melhores_meses = st.text_input('Melhores Meses', '')
meses_sazonalidade = st.text_input('Meses de Sazonalidade', '')

# Botão para calcular
if st.button('Calcular'):
    if all([valor_imovel, entrada_percentual, taxa_juros, prazo_anos, renda_desejada, valor_diaria, custos_fixos, qtd_imoveis, taxa_administracao, valor_reserva_emergencia]):
        # Cálculos
        valor_parcela = calcular_parcela(valor_imovel, entrada, taxa_juros, prazo_anos)
        receita_mensal_total, custo_administracao, reserva_emergencia, total_custos_mensais, lucro_mensal = calcular_renda(
            valor_diaria, qtd_imoveis, 30, custos_fixos, taxa_administracao, valor_reserva_emergencia
        )
        tempo_dias = tempo_para_alcancar(valor_parcela, valor_diaria, qtd_imoveis)
        valor_total_pago = calcular_valor_total_pago(valor_parcela, prazo_anos)
        valor_reinvestir = lucro_mensal * (percentual_reinvestir / 100)
        lucro_nao_distribuido = lucro_mensal - valor_reinvestir

        # Resultados
        tabelas = [
            ('Tabela de Financiamento Imobiliário', [
                ['Valor do Imóvel', formatar_valor(valor_imovel, moeda)],
                ['Entrada (%)', f'{entrada_percentual}%'],
                ['Taxa de Juros Anual', f'{taxa_juros}%'],
                ['Valor da Parcela (aprox.)', formatar_valor(valor_parcela, moeda)],
                ['Valor da Parcela em 10 anos (aprox.)', formatar_valor(calcular_parcela(valor_imovel, entrada, taxa_juros, 10), moeda)],
                ['Valor da Parcela em 5 anos (aprox.)', formatar_valor(calcular_parcela(valor_imovel, entrada, taxa_juros, 5), moeda)],
                ['Valor Total Pago ao Final do Financiamento', formatar_valor(valor_total_pago, moeda)]
            ]),
            ('Tabela de Renda Airbnb', [
                ['Renda Desejada', formatar_valor(renda_desejada, moeda)],
                ['Diária por Imóvel', formatar_valor(valor_diaria, moeda)],
                ['Receita Mensal Total (1 imóvel)', formatar_valor(receita_mensal_total, moeda)]
            ]),
            ('Tempo para Alcançar o Valor da Parcela', [
                ['Período de Amortização', f'{prazo_anos} anos'],
                ['Valor da Parcela', formatar_valor(valor_parcela, moeda)],
                ['Tempo para Alcançar o Valor da Parcela (dias)', tempo_dias]
            ]),
            ('Receita Líquida e Lucro Após Custos', [
                ['Receita Mensal Total', formatar_valor(receita_mensal_total, moeda)],
                ['Custos Fixos Mensais', formatar_valor(custos_fixos, moeda)],
                ['Valor da Parcela', formatar_valor(valor_parcela, moeda)],
                ['Administração', formatar_valor(custo_administracao, moeda)],
                ['Reserva de Emergência', formatar_valor(reserva_emergencia, moeda)],
                ['Total de Custos Mensais', formatar_valor(total_custos_mensais, moeda)],
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

        # Mostrar Introdução e Resultados
        st.write("""
        ### Resultados Gerados com Sucesso!

        O cálculo foi realizado com base nas informações fornecidas. Confira os detalhes abaixo e ajuste qualquer valor, se necessário. Você pode recalcular a qualquer momento, alterando os valores nos campos acima e clicando em "Calcular" novamente. Se precisar de ajuda, estamos à disposição! Se tiver qualquer dúvida ou sugestão, pode enviar uma mensagem para o meu WhatsApp: (91) 99942-5135.
        """)

        # Mostrar Tabelas na Interface
        for titulo, tabela in tabelas:
            df = pd.DataFrame(tabela, columns=['Descrição', 'Valores'])
            st.write(f"### {titulo}")
            st.dataframe(df)
    else:
        st.warning("Por favor, preencha todos os campos antes de calcular.")
