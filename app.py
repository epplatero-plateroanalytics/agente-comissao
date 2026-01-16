import streamlit as st
import pandas as pd
import plotly.express as px
from jinja2 import Environment, FileSystemLoader
import pdfkit
import tempfile
from io import BytesIO

st.set_page_config(page_title="Agente de Comissões", layout="wide")

st.title("Agente de Comissões – Dashboard e Relatório PDF")

st.write("Envie uma ou mais planilhas de comissão (XLSX ou CSV).")

arquivos = st.file_uploader(
    "Selecione os arquivos",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

def limpar_df(df):
    df = df.rename(columns={
        "DATA": "DATA",
        "CLIENTE": "CLIENTE",
        "VALOR DO PEDIDO": "VALOR_DO_PEDIDO"
    })
    df = df[df["CLIENTE"].notna()]
    df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
    df = df[df["DATA"].notna()]
    df["ANO"] = df["DATA"].dt.year
    df["MES"] = df["DATA"].dt.month
    return df

df_total = None

if arquivos:
    dfs = []
    for arq in arquivos:
        if arq.name.endswith(".xlsx"):
            df = pd.read_excel(arq)
        else:
            df = pd.read_csv(arq, sep=";")
        dfs.append(df)

    df_total = pd.concat(dfs, ignore_index=True)
    df_total = limpar_df(df_total)

    st.subheader("Prévia dos dados combinados")
    st.dataframe(df_total.head())

    total_vendas = df_total["VALOR_DO_PEDIDO"].sum()
    ticket_medio = df_total["VALOR_DO_PEDIDO"].mean()
    total_pedidos = len(df_total)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Vendas", f"R$ {total_vendas:,.2f}")
    col2.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
    col3.metric("Total de Pedidos", total_pedidos)

    ranking = (
        df_total.groupby("CLIENTE")["VALOR_DO_PEDIDO"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("Top 10 Clientes por Valor de Vendas")
    st.dataframe(ranking.reset_index().rename(columns={"VALOR_DO_PEDIDO": "TOTAL_VENDAS"}))

    df_mensal = (
        df_total
        .groupby(["ANO", "MES"])["VALOR_DO_PEDIDO"]
        .sum()
        .reset_index()
    )
    df_mensal["PERIODO"] = df_mensal["ANO"].astype(str) + "-" + df_mensal["MES"].astype(str).str.zfill(2)

    fig = px.line(
        df_mensal,
        x="PERIODO",
        y="VALOR_DO_PEDIDO",
        title="Evolução Mensal de Vendas"
    )
    st.subheader("Evolução Mensal de Vendas")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Relatório em PDF")

    if st.button("Gerar relatório em PDF"):
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("relatorio.html")

        ranking_html = ranking.reset_index().rename(
            columns={"VALOR_DO_PEDIDO": "TOTAL_VENDAS"}
        ).to_html(index=False)

        html = template.render(
            total_vendas=f"{total_vendas:,.2f}",
            ticket_medio=f"{ticket_medio:,.2f}",
            total_pedidos=total_pedidos,
            ranking_html=ranking_html
        )

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
            pdfkit.from_string(html, tmp_pdf.name)
            tmp_pdf.seek(0)
            pdf_bytes = tmp_pdf.read()

        st.download_button(
            "Baixar relatório em PDF",
            data=pdf_bytes,
            file_name="relatorio_comissoes.pdf",
            mime="application/pdf",
        )
else:
    st.info("Envie pelo menos uma planilha para começar.")
