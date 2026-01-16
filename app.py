import streamlit as st
import pandas as pd

from core.cleaner import limpar_planilha
from core.utils import detectar_tipos
from core.insights import gerar_kpis, gerar_insights
from core.dashboard.filters import aplicar_filtros
from core.email.excel_exporter import exportar_excel
from core.email.email_sender import enviar_email_com_anexo
from core.pdf.pdf_engine_cloud import gerar_pdf


st.set_page_config(
    page_title="Relatório Premium — Platero Analytics",
    layout="wide"
)

st.title("Agente Universal PRO — Platero Analytics")
st.write("Envie uma planilha para gerar um Relatório Premium completo.")


# Upload
arquivo = st.file_uploader("Selecione um arquivo", type=["xlsx", "csv"])

if not arquivo:
    st.info("Envie uma planilha para começar.")
    st.stop()

nome = arquivo.name.lower()

try:
    if nome.endswith(".xlsx"):
        df = pd.read_excel(arquivo)
    else:
        try:
            df = pd.read_csv(arquivo, sep=";")
        except:
            df = pd.read_csv(arquivo)
except Exception as e:
    st.error(f"Erro ao ler o arquivo: {e}")
    st.stop()

if df.empty:
    st.error("A planilha está vazia.")
    st.stop()


# Limpeza
df = limpar_planilha(df)

if df.empty:
    st.error("Após limpeza, a planilha ficou vazia.")
    st.stop()


# Tipos
datas, numericas, categoricas = detectar_tipos(df)


# Dashboard com filtros
df_filtrado = aplicar_filtros(df, datas, numericas, categoricas)


# KPIs
kpis = gerar_kpis(df_filtrado, numericas)


# Insights
insights = gerar_insights(df_filtrado, datas, numericas, categoricas)


# Botão PDF
st.subheader("📄 Relatório Premium")
if st.button("Gerar Relatório Premium"):
    pdf_bytes = gerar_pdf(
        df=df,
        df_filtrado=df_filtrado,
        datas=datas,
        numericas=numericas,
        categoricas=categoricas,
        kpis=kpis,
        insights=insights
    )

    st.success("PDF Premium gerado com sucesso!")

    st.download_button(
        "Baixar Relatório Premium",
        data=pdf_bytes,
        file_name="relatorio_premium.pdf",
        mime="application/pdf"
    )


# Exportação Excel
st.subheader("📤 Exportar Dados")
if st.button("Exportar Excel"):
    excel_bytes = exportar_excel(df_filtrado)
    st.download_button(
        "Baixar Excel",
        data=excel_bytes,
        file_name="dados_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# Envio por e-mail
st.subheader("📧 Enviar por E-mail")

with st.form("email_form"):
    destinatario = st.text_input("E-mail do destinatário")
    assunto = st.text_input("Assunto", "Relatório Premium — Platero Analytics")
    mensagem = st.text_area("Mensagem", "Segue em anexo o relatório premium.")

    enviar = st.form_submit_button("Enviar E-mail")

    if enviar:
        pdf_bytes = gerar_pdf(
            df=df,
            df_filtrado=df_filtrado,
            datas=datas,
            numericas=numericas,
            categoricas=categoricas,
            kpis=kpis,
            insights=insights
        )

        sucesso = enviar_email_com_anexo(
            destinatario=destinatario,
            assunto=assunto,
            mensagem=mensagem,
            anexo_bytes=pdf_bytes,
            nome_arquivo="relatorio_premium.pdf"
        )

        if sucesso:
            st.success("E-mail enviado com sucesso!")
        else:
            st.error("Falha ao enviar o e-mail.")