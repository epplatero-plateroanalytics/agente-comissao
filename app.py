import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Agente Universal de Planilhas", layout="wide")

st.title("Agente Universal de Planilhas – Exploração e Análise Automática")
st.write("Envie uma planilha em XLSX ou CSV e o agente fará a análise automaticamente.")

# ---------------------------
# 1. Upload do arquivo
# ---------------------------
arquivo = st.file_uploader(
    "Selecione um arquivo",
    type=["xlsx", "csv"],
    accept_multiple_files=False
)

if not arquivo:
    st.info("Envie uma planilha para começar.")
    st.stop()

# ---------------------------
# 2. Leitura segura da planilha
# ---------------------------
nome = arquivo.name.lower()

try:
    if nome.endswith(".xlsx"):
        df = pd.read_excel(arquivo)
    else:
        try:
            df = pd.read_csv(arquivo, sep=";")
        except Exception:
            df = pd.read_csv(arquivo)
except Exception:
    st.error("Não foi possível ler o arquivo. Verifique se ele está corrompido ou protegido.")
    st.stop()

# ---------------------------
# 3. Validações automáticas
# ---------------------------

# Planilha vazia
if df.empty:
    st.error("A planilha enviada está vazia.")
    st.stop()

# Sem colunas
if len(df.columns) == 0:
    st.error("A planilha não possui colunas.")
    st.stop()

# Colunas duplicadas
if df.columns.duplicated().any():
    st.warning("Foram encontradas colunas duplicadas. Elas foram renomeadas automaticamente.")
    df.columns = [f"{col}_{i}" if df.columns.tolist().count(col) > 1 else col
                  for i, col in enumerate(df.columns)]

# ---------------------------
# 4. Conversão automática de tipos
# ---------------------------

# Detectar datas
datas = []
for col in df.columns:
    try:
        convertido = pd.to_datetime(df[col], errors="raise", dayfirst=True)
        df[col] = convertido
        datas.append(col)
    except Exception:
        pass

# Detectar numéricas (incluindo números como texto)
for col in df.columns:
    if df[col].dtype == object:
        try:
            df[col] = df[col].str.replace(".", "").str.replace(",", ".").astype(float)
        except Exception:
            pass

numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()

# ---------------------------
# 5. Exibição inicial
# ---------------------------
st.subheader("Prévia dos dados")
st.dataframe(df.head())

st.markdown(f"**Linhas:** {df.shape[0]} &nbsp;&nbsp; **Colunas:** {df.shape[1]}")

st.subheader("Tipos de colunas detectados")
col1, col2, col3 = st.columns(3)
col1.write("**Numéricas:**")
col1.write(numericas if numericas else "-")
col2.write("**Datas:**")
col2.write(datas if datas else "-")
col3.write("**Categóricas/Textos:**")
col3.write(categoricas if categoricas else "-")

# ---------------------------
# 6. Resumo estatístico
# ---------------------------
st.subheader("Resumo estatístico das colunas numéricas")
if numericas:
    st.dataframe(df[numericas].describe().T)
else:
    st.info("Nenhuma coluna numérica encontrada.")

# ---------------------------
# 7. Exploração visual
# ---------------------------
st.header("Exploração visual")
aba1, aba2, aba3 = st.tabs(["Séries temporais", "Comparações por categoria", "Distribuições"])

# ---------------------------
# 7.1 Séries temporais
# ---------------------------
with aba1:
    if datas and numericas:
        col_data = st.selectbox("Escolha a coluna de data", datas)
        col_valor = st.selectbox("Escolha a coluna numérica", numericas)
        freq = st.selectbox("Agregação", ["Diário", "Mensal", "Anual"])

        df_temp = df[[col_data, col_valor]].dropna()

        # Se houver datas duplicadas, agregamos automaticamente
        if df_temp[col_data].duplicated().any():
            st.warning("Datas duplicadas detectadas. Valores agregados automaticamente.")
            df_temp = df_temp.groupby(col_data)[col_valor].sum().reset_index()

        df_temp = df_temp.sort_values(by=col_data, ignore_index=True)

        if freq == "Mensal":
            df_temp["__PERIODO__"] = df_temp[col_data].dt.to_period("M").dt.to_timestamp()
        elif freq == "Anual":
            df_temp["__PERIODO__"] = df_temp[col_data].dt.to_period("Y").dt.to_timestamp()
        else:
            df_temp["__PERIODO__"] = df_temp[col_data]

        df_group = df_temp.groupby("__PERIODO__")[col_valor].sum().reset_index()

        fig = px.line(df_group, x="__PERIODO__", y=col_valor,
                      title=f"Evolução de {col_valor} ao longo do tempo")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("É preciso ter pelo menos uma coluna de data e uma numérica.")

# ---------------------------
# 7.2 Comparações por categoria
# ---------------------------
with aba2:
    if categoricas and numericas:
        col_cat = st.selectbox("Escolha a coluna categórica", categoricas)
        col_valor = st.selectbox("Escolha a coluna numérica", numericas, key="cat_num")
        tipo_agreg = st.selectbox("Tipo de agregação", ["Soma", "Média", "Contagem"])

        df_cat = df[[col_cat, col_valor]].dropna()

        # Limitar categorias muito numerosas
        if df_cat[col_cat].nunique() > 200:
            st.warning("Muitas categorias detectadas. Exibindo apenas as 200 mais frequentes.")
            top = df_cat[col_cat].value_counts().head(200).index
            df_cat = df_cat[df_cat[col_cat].isin(top)]

        if tipo_agreg == "Soma":
            df_group = df_cat.groupby(col_cat)[col_valor].sum().reset_index()
        elif tipo_agreg == "Média":
            df_group = df_cat.groupby(col_cat)[col_valor].mean().reset_index()
        else:
            df_group = df_cat.groupby(col_cat)[col_valor].count().reset_index()
            df_group = df_group.rename(columns={col_valor: "Contagem"})
            col_valor = "Contagem"

        df_group = df_group.sort_values(df_group.columns[1], ascending=False)

        fig = px.bar(df_group, x=col_cat, y=df_group.columns[1],
                     title=f"{tipo_agreg} de {col_valor} por {col_cat}")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_group)
    else:
        st.info("É preciso ter pelo menos uma coluna categórica e uma numérica.")

# ---------------------------
# 7.3 Distribuições numéricas
# ---------------------------
with aba3:
    if numericas:
        col_num = st.selectbox("Escolha a coluna numérica", numericas, key="dist_num")
        fig = px.histogram(df, x=col_num, nbins=30, title=f"Distribuição de {col_num}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhuma coluna numérica encontrada.")import streamlit as st
import pandas as pd
import plotly.express as px
import pdfkit
import base64
import tempfile

st.set_page_config(page_title="Agente Universal – PDF + Insights", layout="wide")

st.title("Agente Universal de Planilhas – PDF + Insights Automáticos")
st.write("Envie uma planilha e receba análises, gráficos, insights e um relatório em PDF.")

# ---------------------------
# 1. Upload
# ---------------------------
arquivo = st.file_uploader("Selecione um arquivo", type=["xlsx", "csv"])

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
# 5. Exibição inicial
# ---------------------------
st.subheader("Prévia dos dados")
st.dataframe(df.head())

# ---------------------------
# 6. Insights automáticos
# ---------------------------
st.header("🧠 Insights automáticos")

insights = []

if numericas:
    for col in numericas:
        media = df[col].mean()
        maximo = df[col].max()
        minimo = df[col].min()
        insights.append(f"- A média de **{col}** é {media:,.2f}.")
        insights.append(f"- O maior valor registrado em **{col}** é {maximo:,.2f}.")
        insights.append(f"- O menor valor registrado em **{col}** é {minimo:,.2f}.")

if datas:
    col_data = datas[0]
    inicio = df[col_data].min()
    fim = df[col_data].max()
    insights.append(f"- O período analisado vai de **{inicio.date()}** até **{fim.date()}**.")

if categoricas:
    col_cat = categoricas[0]
    top_cat = df[col_cat].value_counts().idxmax()
    insights.append(f"- A categoria mais frequente em **{col_cat}** é **{top_cat}**.")

if not insights:
    insights.append("Nenhum insight automático pôde ser gerado.")

for item in insights:
    st.write(item)

# ---------------------------
# 7. Gráficos
# ---------------------------
st.header("📊 Gráficos automáticos")

graficos_html = ""

if numericas:
    col_num = st.selectbox("Escolha uma coluna numérica", numericas)
    fig = px.histogram(df, x=col_num, nbins=30, title=f"Distribuição de {col_num}")
    st.plotly_chart(fig, use_container_width=True)
    graficos_html += fig.to_html(full_html=False)

if datas and numericas:
    col_data = datas[0]
    col_valor = numericas[0]
    df_temp = df[[col_data, col_valor]].dropna()
    df_temp = df_temp.sort_values(by=col_data)

    fig2 = px.line(df_temp, x=col_data, y=col_valor, title=f"Evolução de {col_valor} ao longo do tempo")
    st.plotly_chart(fig2, use_container_width=True)
    graficos_html += fig2.to_html(full_html=False)

# ---------------------------
# 8. Gerar PDF
# ---------------------------
st.header("📄 Gerar relatório em PDF")

html = f"""
<h1>Relatório Automático</h1>
<h2>Insights</h2>
{''.join(f'<p>{i}</p>' for i in insights)}

<h2>Gráficos</h2>
{graficos_html}

<h2>Primeiras linhas da planilha</h2>
{df.head().to_html()}
"""

if st.button("Gerar PDF"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
        tmp_html.write(html.encode("utf-8"))
        tmp_html_path = tmp_html.name

    pdf_path = tmp_html_path.replace(".html", ".pdf")
    pdfkit.from_file(tmp_html_path, pdf_path)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()

    st.success("PDF gerado com sucesso!")
    st.download_button("Baixar PDF", data=pdf_bytes, file_name="relatorio.pdf")