import streamlit as st
import pandas as pd

from cleaner import limpar_planilha
from utils import detectar_tipos
from layout import render_layout
from pdf_engine_cloud import gerar_pdf


st.set_page_config(
    page_title="Relatório Premium — Platero Analytics",
    layout="wide"
)

st.title("Agente Universal PRO — Platero Analytics")
st.write("Envie uma planilha para gerar um Relatório Premium completo.")


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


df = limpar_planilha(df)

if df.empty:
    st.error("Após limpeza, a planilha ficou vazia.")
    st.stop()


datas, numericas, categoricas = detectar_tipos(df)

df_filtrado = render_layout(df, datas, numericas, categoricas, lang="pt")


if st.session_state.get("pdf_ready"):
    figs = st.session_state.get("figs_pdf", [])

    try:
        pdf_bytes = gerar_pdf(
            df=df,
            df_filtrado=df_filtrado,
            datas=datas,
            numericas=numericas,
            categoricas=categoricas,
            figs=figs,
            lang="pt"
        )

        st.success("PDF Premium gerado com sucesso!")

        st.download_button(
            "Baixar Relatório Premium",
            data=pdf_bytes,
            file_name="relatorio_premium.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")

    st.session_state["pdf_ready"] = False