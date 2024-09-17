import smtplib
from email.message import EmailMessage
import os
from io import BytesIO
import streamlit as st
import pandas as pd

def enviar_email(para, assunto, corpo, anexo=None):
    # Obter credenciais e informações do servidor SMTP das variáveis de ambiente
    email_user = os.getenv('EMAIL_USER')
    email_senha = os.getenv('EMAIL_PASS')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))

    msg = EmailMessage()
    msg.set_content(corpo)
    msg['Subject'] = assunto
    msg['From'] = email_user
    msg['To'] = para

    if anexo:
        anexo.seek(0)  # Garantir que estamos no início do arquivo
        msg.add_attachment(anexo.read(), maintype='application', subtype='pdf', filename='recibo.pdf')

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_senha)
            server.send_message(msg)
        print(f"E-mail enviado com sucesso para {para}")
        return None
    except Exception as e:
        print(f"Erro ao enviar e-mail para {para}: {e}")
        return str(e)
    return None

# Interface Streamlit
st.title('Sistema de Envio de Recibos')

# Upload de arquivo de recibo
uploaded_file = st.file_uploader("Carregue o arquivo do recibo (PDF)", type="pdf")

if uploaded_file:
    st.success("Arquivo do recibo carregado com sucesso!")

    # Inserção manual de dados dos colaboradores
    st.subheader("Insira os dados dos colaboradores")

    # Adicionar campos para e-mail e nome
    st.write("Preencha os dados dos colaboradores e clique em 'Adicionar Colaborador'")

    email_colaboradores = []
    nome_colaboradores = []
    
    with st.form(key='colaboradores_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            email_input = st.text_input("E-mail do colaborador")
        with col2:
            nome_input = st.text_input("Nome do colaborador")

        add_colaborador = st.form_submit_button("Adicionar Colaborador")

        if add_colaborador and email_input and nome_input:
            email_colaboradores.append(email_input)
            nome_colaboradores.append(nome_input)
            st.success(f"Colaborador {nome_input} adicionado com sucesso!")
        elif add_colaborador:
            st.warning("Por favor, preencha ambos os campos.")

    if email_colaboradores:
        st.write("Lista de colaboradores:")
        colaboradores_df = pd.DataFrame({
            'Email': email_colaboradores,
            'Nome': nome_colaboradores
        })
        st.dataframe(colaboradores_df)

        # Botão para enviar e-mail para o destinatário específico
        if st.button("Enviar Recibo para destinatário específico"):
            st.info("Enviando recibo para o destinatário específico, por favor, aguarde...")

            email_destinatario = 'adriaelmendes@gmail.com'
            nome_destinatario = 'Destinatário'  # Altere conforme necessário
            corpo_email = f"Olá {nome_destinatario},\n\nSegue em anexo o seu recibo salarial.\n\nAtenciosamente,\nSua Empresa"

            erro = enviar_email(email_destinatario, "Seu Recibo Salarial", corpo_email, uploaded_file)
            if erro:
                st.error(f"Erro ao enviar para {email_destinatario}: {erro}")
            else:
                st.success(f"Recibo enviado com sucesso para {email_destinatario}!")

        if st.button("Enviar Recibos para Colaboradores"):
            st.info("Enviando recibos para colaboradores, por favor, aguarde...")

            erros = []
            sucesso = []
            
            for index, row in colaboradores_df.iterrows():
                email = row['Email']
                nome = row['Nome']
                
                corpo_email = f"Olá {nome},\n\nSegue em anexo o seu recibo salarial.\n\nAtenciosamente,\nSua Empresa"
                
                erro = enviar_email(email, "Seu Recibo Salarial", corpo_email, uploaded_file)
                if erro:
                    erros.append((email, erro))
                else:
                    sucesso.append(email)
            
            if sucesso:
                st.success(f"Recibos enviados com sucesso para {len(sucesso)} colaboradores!")

            if erros:
                st.error(f"Ocorreram erros ao enviar para {len(erros)} colaboradores. Veja detalhes abaixo:")
                for email, erro in erros:
                    st.write(f"Erro ao enviar para {email}: {erro}")

    else:
        st.info("Adicione colaboradores para enviar os recibos.")
