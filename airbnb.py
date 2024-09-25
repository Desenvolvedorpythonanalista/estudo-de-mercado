import streamlit as st
import pandas as pd
import numpy as np
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
    parcela = (valor_financiado * taxa_juros_mensal * (1 + taxa_juros_mensal) ** prazo_meses) / \
              ((1 + taxa_juros_mensal) ** prazo_meses - 1)
    return parcela, valor_financiado

# Função para calcular a receita mensal e lucro
def calcular_renda(valor_aluguel, qtd_imoveis, custos_fixos, taxa_administracao, 
                   valor_reserva_emergencia, taxa_condominial, iptu, valor_imovel, entrada, taxa_juros, prazo_anos):
    receita_mensal_total = valor_aluguel * qtd_imoveis
    custo_administracao = receita_mensal_total * (taxa_administracao / 100)
    valor_parcela = calcular_parcela(valor_imovel, entrada, taxa_juros, prazo_anos)[0]
    
    total_custos_mensais = (custos_fixos + valor_parcela + custo_administracao + 
                            valor_reserva_emergencia + taxa_condominial + iptu)
    lucro_mensal = receita_mensal_total - total_custos_mensais
    return receita_mensal_total, custo_administracao, total_custos_mensais, lucro_mensal, valor_parcela

# Função para calcular o tempo necessário para alcançar o valor da entrada
def tempo_para_alcancar(valor_entrada, lucro_mensal):
    return valor_entrada / lucro_mensal if lucro_mensal > 0 else float('inf')

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
        table = Table(data, colWidths=[250, 150])
        
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

# Filtro para selecionar tipo de investimento
tipo_investimento = st.sidebar.selectbox('Selecione o Tipo de Investimento', ['Imóveis no Brasil', 'Investimentos no Exterior'])

if tipo_investimento == 'Imóveis no Brasil':
    st.write(""" 
    ### Bem-vindo à nossa Simulação de Investimentos Imobiliários no Brasil! 

    Esta ferramenta ajuda você a avaliar a viabilidade financeira do seu investimento imobiliário, 
    calculando parcelas de financiamento e potencial de lucro com aluguel.
    """)

    # Campos de entrada
    valor_imovel = st.number_input('Valor do Imóvel', value=0, step=1000, format="%d")
    entrada_percentual = st.slider('Entrada (%)', 0, 100, 0)
    entrada = valor_imovel * entrada_percentual / 100 if valor_imovel else 0
    taxa_juros = st.number_input('Taxa de Juros Anual (%)', value=0.0, step=0.1, format="%.1f")
    prazo_anos = st.number_input('Prazo do Financiamento (anos)', value=0, step=1)
    valor_aluguel = st.number_input('Valor do Aluguel (Mensal)', value=0, step=10)
    custos_fixos = st.number_input('Custos Fixos Mensais', value=3000, step=100)
    taxa_administracao = st.number_input('Taxa de Administração (%)', value=2.8, step=0.5)
    valor_reserva_emergencia = st.number_input('Valor para Reserva de Emergência', value=200, step=10)
    taxa_condominial = st.number_input('Taxa Condominial', value=1500, step=10)
    iptu = st.number_input('Valor do IPTU', value=800, step=10)
    irrf_percentual = st.number_input('Alíquota do IRRF (%)', value=0.0, step=0.5)

    # Campos adicionais com checkboxes
    show_opcionais = st.checkbox("Mostrar campos adicionais")
    if show_opcionais:
        regras_casa = st.text_input('Regras da Casa', '')
        faixa_etaria = st.text_input('Faixa Etária Preferida', '')
        melhores_meses = st.text_input('Melhores Meses', '')
        meses_sazonalidade = st.text_input('Meses de Sazonalidade', '')
        recomendacoes_melhorias = st.text_input('Recomendações e Melhorias do Mês', '')
        gastos_cortados = st.text_input('Gastos que Podem Ser Cortados', '')
        problemas_encontrados = st.text_input('Problemas Encontrados', '')

    # Botão para calcular
    if st.button('Calcular'):
        # Verifica se todos os campos obrigatórios estão preenchidos
        if all([valor_imovel, entrada_percentual, taxa_juros, prazo_anos, valor_aluguel,
                 custos_fixos, taxa_administracao, valor_reserva_emergencia,
                 taxa_condominial, iptu]):
            
            # Cálculos
            valor_parcela, valor_financiado = calcular_parcela(valor_imovel, entrada, taxa_juros, prazo_anos)
            receita_mensal_total, custo_administracao, total_custos_mensais, lucro_mensal, valor_parcela = calcular_renda(
                valor_aluguel, 1, custos_fixos, taxa_administracao, 
                valor_reserva_emergencia, taxa_condominial, iptu, valor_imovel, entrada, taxa_juros, prazo_anos
            )
            
            # Cálculo do IRRF
            irrf_valor = (lucro_mensal * (irrf_percentual / 100)) if lucro_mensal > 0 else 0
            lucro_liquido = lucro_mensal - irrf_valor
            
            # Cálculo do tempo necessário para alcançar o valor da entrada
            tempo_retorno = tempo_para_alcancar(entrada, valor_aluguel)
            
            # Verifica se o tempo de retorno é infinito
            if tempo_retorno == float('inf'):
                tempo_retorno_formatado = "Nunca"
            else:
                tempo_retorno_formatado = f"{int(tempo_retorno)} meses"
            
            # Cálculo do total pago ao final do financiamento
            total_pago = calcular_valor_total_pago(valor_parcela, prazo_anos)

            # Tabela de Resultados (Cálculo do Financiamento)
            tabela_financiamento = [
                ["Descrição", "Valor"],
                ["Valor do Imóvel", formatar_valor(valor_imovel, 'BRL')],
                ["Entrada", formatar_valor(entrada, 'BRL')],
                ["Valor Financiado", formatar_valor(valor_financiado, 'BRL')],
                ["Taxa de Juros", f"{taxa_juros:.2f}%"],
                ["Prazo do Financiamento (meses)", prazo_anos * 12],
                ["Parcela Mensal", formatar_valor(valor_parcela, 'BRL')],
                ["Total Pago Financiado", formatar_valor(total_pago, 'BRL')],  # Total pago com juros
            ]
            
            # Tabela de Resultados (Total Pago e Lucro)
            tabela_lucro = [
                ["Descrição", "Valor"],
                ["Valor do Aluguel", formatar_valor(valor_aluguel, 'BRL')],
                ["Custo Fixo Mensal", formatar_valor(custos_fixos, 'BRL')],
                ["Custo de Administração", formatar_valor(custo_administracao, 'BRL')],
                ["Reserva de Emergência", formatar_valor(valor_reserva_emergencia, 'BRL')],
                ["Taxa Condominial", formatar_valor(taxa_condominial, 'BRL')],
                ["IPTU", formatar_valor(iptu, 'BRL')],
                ["Valor da Parcela", formatar_valor(valor_parcela, 'BRL')],
                ["Total de Custos Mensais", formatar_valor(total_custos_mensais, 'BRL')],
                ["Lucro Mensal", formatar_valor(lucro_mensal, 'BRL')],
                ["Imposto de Renda (IRRF)", formatar_valor(irrf_valor, 'BRL')],
                ["Lucro Líquido", formatar_valor(lucro_liquido, 'BRL')],
                ["Tempo para Alcançar a Entrada", tempo_retorno_formatado],
            ]
            
            # Exibe as tabelas
            st.subheader("Cálculo do Financiamento")
            st.table(pd.DataFrame(tabela_financiamento[1:], columns=tabela_financiamento[0]))
            st.subheader("Total Pago e Lucro")
            st.table(pd.DataFrame(tabela_lucro[1:], columns=tabela_lucro[0]))
            
            # Geração do PDF
            pdf = gerar_pdf([("Cálculo do Financiamento", tabela_financiamento), ("Total Pago e Lucro", tabela_lucro)])
            st.download_button('Baixar PDF', pdf, 'simulacao_investimento.pdf')

        else:
            st.warning("Por favor, preencha todos os campos obrigatórios.")

else:
    st.write(""" 
    ### Selecione uma opção no menu à esquerda para começar a simulação!
    """)


if tipo_investimento == 'Investimentos no Exterior':
    st.write(""" 
    ### Investimentos em Imóveis nos EUA

    Investir em imóveis no Brasil pode apresentar algumas desvantagens quando comparado aos Estados Unidos. Aqui estão três problemas principais:

    1. **Baixa Rentabilidade**: Ao investir em imóveis para aluguel no Brasil, a rentabilidade pode ser de apenas 0,5% a 1% ao mês. Após considerar as despesas, a receita líquida pode ser praticamente inexistente.
    
    2. **Valorização a Longo Prazo**: Comprar imóveis na planta visa a valorização entre a compra e a entrega, mas isso pode levar anos até que você veja um retorno real. O lucro só é realizado na venda, o que torna o processo lento e arriscado.
    
    3. **Construção e Financiamento Difíceis**: Construir um imóvel envolve riscos consideráveis. Além disso, obter financiamento pode ser complicado e caro, não sendo acessível a todos.

    Ao considerar investir em imóveis, os Estados Unidos oferecem oportunidades únicas. Aqui estão algumas vantagens:

    - **Facilidade de Financiamento**: Nos EUA, é possível realizar operações de compra, reforma ou construção sem um histórico de crédito. Isso facilita o acesso ao mercado para novos investidores.

    - **Propriedades Multifamiliares**: Ao investir em imóveis multifamiliares, você se torna proprietário do prédio inteiro. Os aluguéis de curto prazo permitem maior flexibilidade e capacidade de troca de inquilinos.

    - **Valorização e Controle**: Imóveis comerciais (acima de 5 unidades) podem ser reformados para aumentar seu valor e controle sobre a receita do aluguel.

    Se você estiver pensando em investir em imóveis, considere o mercado imobiliário dos EUA como uma opção viável.
    """)

    # Campos para o usuário inserir os dados
    custo_pedido = st.number_input("Custo do Prédio/Casa (USD):", min_value=0.0, format="%.2f")
    unidades = st.number_input("Número de Unidades:", min_value=1, format="%d")
    aluguel_mensal_unidade = st.number_input("Aluguel Mensal por Unidade (USD):", min_value=0.0, format="%.2f")
    
    # Campo para a porcentagem financiada
    porcentagem_financiada = st.number_input("Porcentagem Financiada do Custo do Prédio (%):", min_value=0.0, max_value=100.0, format="%.2f") / 100

    custo_reforma = st.number_input("Custo da Reforma (USD):", min_value=0.0, format="%.2f")
    juros = st.number_input("Taxa de Juros Anual (%):", min_value=0.0, format="%.2f") / 100
    valor_documentacao = st.number_input("Valor Gasto com Documentação (USD):", min_value=0.0, format="%.2f")
    valorizacao_percentual = st.number_input("Valorização (%) :", min_value=0.0, format="%.2f") / 100

    aliquota_irrf = st.number_input("Aliquota do IRRF (%) :", min_value=0.0, format="%.2f") / 100
    anos_financiamento = st.number_input("Anos de Financiamento:", min_value=1, format="%d")

    # Cálculo do custo total do projeto
    custo_total = custo_pedido + custo_reforma + valor_documentacao

    # Cálculo do financiamento e investimento próprio
    valor_financiamento = porcentagem_financiada * custo_total  # Porcentagem financiada do custo total
    investimento_proprio = custo_total - valor_financiamento  # Investimento próprio

    # Cálculo do valor de venda após valorização
    valor_venda = (custo_pedido + custo_reforma) * (1 + valorizacao_percentual)

    # Cálculo de aluguel total
    aluguel_mensal_total = aluguel_mensal_unidade * unidades
    aluguel_anual_total = aluguel_mensal_total * 12

    # Cálculo de lucro bruto e líquido
    lucro_bruto = valor_venda - custo_total
    lucro_liquido = lucro_bruto * (1 - aliquota_irrf)  # Lucro líquido considerando IRRF

    # Cálculo da parcela mensal do financiamento
    taxa_juros_mensal = juros / 12
    n_periodos = anos_financiamento * 12

    if taxa_juros_mensal > 0:
        parcela_mensal = (valor_financiamento * taxa_juros_mensal) / (1 - (1 + taxa_juros_mensal) ** -n_periodos)
    else:
        parcela_mensal = valor_financiamento / n_periodos

    # Cálculo do saldo disponível após refinanciamento
    valor_refinanciamento = 0.96 * valor_venda  # 96% do valor de venda
    saldo_disponivel = valor_refinanciamento - valor_financiamento  # Saldo disponível após refinanciamento

    # Tabelas para o cálculo do investimento
    tabelas_investimento = [
        ('Dados do Investimento', [
            ['Descrição', 'Valor (USD)'],
            ['Custo do Prédio', f'${custo_pedido:,.2f}'],
            ['Custo da Reforma', f'${custo_reforma:,.2f}'],
            ['Valor Total do Projeto', f'${custo_total:,.2f}'],
            ['Valor de Venda Após Valorização', f'${valor_venda:,.2f}'],
            ['Juros e Despesas', f'${valor_documentacao:,.2f}'],
            ['Lucro Bruto', f'${lucro_bruto:,.2f}'],
            ['Lucro Líquido', f'${lucro_liquido:,.2f}'],
            ['Aluguel Mensal Total', f'${aluguel_mensal_total:,.2f}'],
            ['Parcela Mensal do Financiamento', f'${parcela_mensal:,.2f}'],
            ['Valor do Financiamento', f'${valor_financiamento:,.2f}'],
            ['Investimento Próprio', f'${investimento_proprio:,.2f}'],
            ['Valor de Refinanciamento (96%)', f'${valor_refinanciamento:,.2f}'],
            ['Saldo Disponível Após Refinanciamento', f'${saldo_disponivel:,.2f}'],
        ]),
        ('Valorização do Imóvel', [
            ['Descrição', 'Valor (%)'],
            ['Valorização Total', f'{valorizacao_percentual * 100:.2f}%'],
            ['Valor Após Valorização (USD)', f'${valor_venda:,.2f}']
        ]),
        ('Cálculo do Lucro', [
            ['Descrição', 'Valor (USD)'],
            ['Lucro Bruto', f'${lucro_bruto:,.2f}'],
            ['Lucro Líquido (após IRRF)', f'${lucro_liquido:,.2f}']
        ]),
        ('Análise de Aluguel', [
            ['Descrição', 'Valor (USD)'],
            ['Aluguel Mensal por Unidade', f'${aluguel_mensal_unidade:,.2f}'],
            ['Aluguel Mensal Total', f'${aluguel_mensal_total:,.2f}'],
            ['Aluguel Anual Total', f'${aluguel_anual_total:,.2f}']
        ]),
        ('Retorno sobre o Investimento (ROI)', [
            ['Descrição', 'Valor (%)'],
            ['Taxa de Retorno (%)', f'{(lucro_liquido / custo_total * 100) if custo_total > 0 else 0:.2f}%']
        ]),
    ]

    # Exibir as tabelas na interface
    for titulo, tabela in tabelas_investimento:
        df = pd.DataFrame(tabela)
        st.write(f"### {titulo}")
        st.dataframe(df)

    # Conversão para reais
    cotacao_dolar = st.number_input("Cotação do Dólar (USD para BRL):", min_value=0.0, format="%.2f")

    # Conversão para reais
    if cotacao_dolar > 0:
        tabelas_reais = [
            ('Dados em Reais', [
                ['Descrição', 'Valor (BRL)'],
                ['Custo do Prédio', f'R$ {custo_pedido * cotacao_dolar:,.2f}'],
                ['Custo da Reforma', f'R$ {custo_reforma * cotacao_dolar:,.2f}'],
                ['Valor Total do Projeto', f'R$ {custo_total * cotacao_dolar:,.2f}'],
                ['Valor de Venda Após Valorização', f'R$ {valor_venda * cotacao_dolar:,.2f}'],
                ['Juros e Despesas', f'R$ {valor_documentacao * cotacao_dolar:,.2f}'],
                ['Lucro Bruto', f'R$ {lucro_bruto * cotacao_dolar:,.2f}'],
                ['Lucro Líquido', f'R$ {lucro_liquido * cotacao_dolar:,.2f}'],
                ['Aluguel Mensal por Unidade', f'R$ {aluguel_mensal_unidade * cotacao_dolar:,.2f}'],
                ['Aluguel Mensal Total', f'R$ {aluguel_mensal_total * cotacao_dolar:,.2f}'],
                ['Parcela Mensal do Financiamento', f'R$ {parcela_mensal * cotacao_dolar:,.2f}'],
                ['Valor de Refinanciamento', f'R$ {valor_refinanciamento * cotacao_dolar:,.2f}'],
                ['Saldo Disponível Após Refinanciamento', f'R$ {saldo_disponivel * cotacao_dolar:,.2f}']
            ])
        ]

        # Exibir as tabelas em reais
        for titulo, tabela in tabelas_reais:
            df_reais = pd.DataFrame(tabela)
            st.write(f"### {titulo}")
            st.dataframe(df_reais)

    # Conclusões
    st.write(""" 
    ### Conclusões sobre o Investimento em Imóveis nos EUA
    
    1. **Crédito Facilitado**: Tanto para a compra quanto para a reforma, o acesso a crédito é simples.
    2. **Saída Fácil**: A venda desse tipo de imóvel é atrativa para fundos de pensão e investidores institucionais.
    3. **Fluxo de Caixa Constante**: No pior cenário, você ainda possui um fluxo de caixa constante.
    4. **Oportunidade de Refinanciamento**: Após a reforma, você pode refinanciar até 96% do valor de mercado.
    
    Ao investir em imóveis nos EUA, você não apenas melhora seu fluxo de caixa, mas também potencializa seu retorno através da valorização do imóvel.
    """)

    # Botão para calcular
    if st.button("Calcular"):
        st.success("Cálculos realizados com sucesso!")

        
