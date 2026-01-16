import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pdfkit
import base64
import tempfile
from datetime import datetime

st.set_page_config(page_title="Agente Universal Premium", layout="wide")

st.title("Agente Universal de Planilhas – Versão Premium + PDF Profissional")
st.write("Envie uma planilha e gere análises avançadas, insights e relatório em PDF.")

# ---------------------------
# 1. Upload
# ---------------------------
arquivo = st.file_uploader("Selecione um arquivo", type=["xlsx", "csv"], key="upload_unico")
if not arquivo:
    st.info("Envie uma planilha para começar.")
    st.stop()

# ---------------------------
# 2. Leitura segura
# ---------------------------
nome = arquivo.name.lower()

try:
    if nome.endswith(".xlsx"):
        df = pd.read_excel(arquivo)
    else:
        try:
            df = pd.read_csv(arquivo, sep=";")
        except:
            df = pd.read_csv(arquivo)
except:
    st.error("Erro ao ler o arquivo.")
    st.stop()

# ---------------------------
# 3. Validações
# ---------------------------
if df.empty:
    st.error("A planilha está vazia.")
    st.stop()

if df.columns.duplicated().any():
    st.warning("Colunas duplicadas detectadas. Renomeando automaticamente.")
    df.columns = [f"{col}_{i}" if df.columns.tolist().count(col) > 1 else col
                  for i, col in enumerate(df.columns)]

# ---------------------------
# 4. Conversão automática
# ---------------------------
datas = []
for col in df.columns:
    try:
        convertido = pd.to_datetime(df[col], errors="raise", dayfirst=True)
        df[col] = convertido
        datas.append(col)
    except:
        pass

for col in df.columns:
    if df[col].dtype == object:
        try:
            df[col] = df[col].str.replace(".", "").str.replace(",", ".").astype(float)
        except:
            pass

numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()

# ---------------------------
# 5. Dashboard Premium
# ---------------------------
st.subheader("Prévia dos dados")
st.dataframe(df.head())

st.subheader("Tipos de colunas detectados")
c1, c2, c3 = st.columns(3)
c1.write(numericas if numericas else "-")
c2.write(datas if datas else "-")
c3.write(categoricas if categoricas else "-")

# ---------------------------
# 6. Insights automáticos
# ---------------------------
st.header("🧠 Insights automáticos")

insights = []

if numericas:
    for col in numericas:
        media = df[col].mean()
        mediana = df[col].median()
        maximo = df[col].max()
        minimo = df[col].min()
        insights.append(f"A média de {col} é {media:,.2f} e a mediana é {mediana:,.2f}.")
        insights.append(f"O maior valor em {col} é {maximo:,.2f} e o menor é {minimo:,.2f}.")

if datas:
    col_data = datas[0]
    inicio = df[col_data].min()
    fim = df[col_data].max()
    insights.append(f"O período analisado vai de {inicio.date()} até {fim.date()}.")

if categoricas:
    col_cat = categoricas[0]
    top_cat = df[col_cat].value_counts().idxmax()
    freq = df[col_cat].value_counts().max()
    insights.append(f"A categoria mais frequente em {col_cat} é {top_cat} ({freq} ocorrências).")

for item in insights:
    st.write("- " + item)

# ---------------------------
# 7. Gráficos (para PDF)
# ---------------------------
graficos_html = ""

if numericas:
    col_num = numericas[0]
    fig = px.histogram(df, x=col_num, nbins=30, title=f"Distribuição de {col_num}")
    st.plotly_chart(fig, use_container_width=True)
    graficos_html += fig.to_html(full_html=False)

if datas and numericas:
    col_data = datas[0]
    col_valor = numericas[0]
    df_temp = df[[col_data, col_valor]].dropna()
    df_temp = df_temp.sort_values(by=col_data)

    fig2 = px.line(df_temp, x=col_data, y=col_valor, title=f"Evolução de {col_valor}")
    st.plotly_chart(fig2, use_container_width=True)
    graficos_html += fig2.to_html(full_html=False)

# ---------------------------
# 8. PDF Profissional
# ---------------------------
st.header("📄 Gerar relatório PDF (Layout Profissional)")

if st.button("Gerar PDF"):
    data_atual = datetime.now().strftime("%d/%m/%Y")

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ text-align: center; color: #003366; }}
            h2 {{ color: #003366; border-bottom: 2px solid #003366; padding-bottom: 5px; }}
            .insight {{ margin: 10px 0; font-size: 14px; }}
            .section {{ margin-top: 40px; }}
            .capa {{
                text-align: center;
                margin-top: 150px;
            }}
            .capa h1 {{ font-size: 40px; }}
            .capa h3 {{ color: #555; }}
        </style>
    </head>
    <body>

    <div class="capa">
        <h1>Relatório Analítico</h1>
        <h3>Gerado em {data_atual}</h3>
        <h4>Agente Universal Premium</h4>
    </div>

    <div class="section">
        <h2>Sumário</h2>
        <p>1. Insights automáticos</p>
        <p>2. Gráficos</p>
        <p>3. Primeiras linhas da planilha</p>
    </div>

    <div class="section">
        <h2>1. Insights automáticos</h2>
        {''.join(f'<p class="insight">• {i}</p>' for i in insights)}
    </div>

    <div class="section">
        <h2>2. Gráficos</h2>
        {graficos_html}
    </div>

    <div class="section">
        <h2>3. Primeiras linhas da planilha</h2>
        {df.head().to_html()}
    </div>

    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
        tmp_html.write(html.encode("utf-8"))
        tmp_html_path = tmp_html.name

    pdf_path = tmp_html_path.replace(".html", ".pdf")
    pdfkit.from_file(tmp_html_path, pdf_path)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.success("PDF gerado com sucesso!")
    st.download_button("Baixar PDF", data=pdf_bytes, file_name="relatorio_profissional.pdf")