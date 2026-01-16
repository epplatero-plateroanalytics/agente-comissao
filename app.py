import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Agente Universal de Planilhas", layout="wide")

st.title("Agente Universal de Planilhas – Exploração e Análise Automática")

st.write("Envie uma planilha em XLSX ou CSV e eu te ajudo a explorar os dados.")

arquivo = st.file_uploader(
    "Selecione um arquivo",
    type=["xlsx", "csv"],
    accept_multiple_files=False
)

if not arquivo:
    st.info("Envie uma planilha para começar.")
    st.stop()

# 1. Leitura genérica da planilha
nome = arquivo.name.lower()
if nome.endswith(".xlsx"):
    df = pd.read_excel(arquivo)
else:
    # tenta ; depois ,
    try:
        df = pd.read_csv(arquivo, sep=";")
    except Exception:
        df = pd.read_csv(arquivo)

st.subheader("Prévia dos dados")
st.dataframe(df.head())

st.markdown(f"**Linhas:** {df.shape[0]} &nbsp;&nbsp; **Colunas:** {df.shape[1]}")

# 2. Identificação de tipos de colunas
numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
datas = df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()

# tenta converter colunas que parecem datas
for col in df.columns:
    if col not in datas:
        try:
            convertido = pd.to_datetime(df[col], errors="raise", dayfirst=True)
            df[col] = convertido
            datas.append(col)
        except Exception:
            pass

categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()

st.subheader("Tipos de colunas detectados")
col1, col2, col3 = st.columns(3)
col1.write("**Numéricas:**")
col1.write(numericas if numericas else "-")
col2.write("**Datas:**")
col2.write(datas if datas else "-")
col3.write("**Categóricas/Textos:**")
col3.write(categoricas if categoricas else "-")

# 3. Resumo estatístico
st.subheader("Resumo estatístico das colunas numéricas")
if numericas:
    st.dataframe(df[numericas].describe().T)
else:
    st.info("Nenhuma coluna numérica encontrada para resumo estatístico.")

# 4. Exploração guiada

st.header("Exploração visual")

aba1, aba2, aba3 = st.tabs(["Séries temporais", "Comparações por categoria", "Distribuições"])

# 4.1 Séries temporais
with aba1:
    if datas and numericas:
        col_data = st.selectbox("Escolha a coluna de data", datas)
        col_valor = st.selectbox("Escolha a coluna numérica para analisar ao longo do tempo", numericas)
        freq = st.selectbox("Agregação", ["Diário", "Mensal", "Anual"])

        df_temp = df[[col_data, col_valor]].dropna()
        df_temp = df_temp.reset_index(drop=True).sort_values(by=col_data)

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
        st.info("É preciso ter pelo menos uma coluna de data e uma numérica para séries temporais.")

# 4.2 Comparações por categoria
with aba2:
    if categoricas and numericas:
        col_cat = st.selectbox("Escolha a coluna categórica", categoricas)
        col_valor = st.selectbox("Escolha a coluna numérica para agregar", numericas, key="cat_num")
        tipo_agreg = st.selectbox("Tipo de agregação", ["Soma", "Média", "Contagem"])

        df_cat = df[[col_cat, col_valor]].dropna()

        if tipo_agreg == "Soma":
            df_group = df_cat.groupby(col_cat)[col_valor].sum().reset_index()
        elif tipo_agreg == "Média":
            df_group = df_cat.groupby(col_cat)[col_valor].mean().reset_index()
        else:
            df_group = df_cat.groupby(col_cat)[col_valor].count().reset_index()
            col_valor = "Contagem"
            df_group = df_group.rename(columns={df_group.columns[1]: col_valor})

        df_group = df_group.sort_values(df_group.columns[1], ascending=False).head(30)

        fig = px.bar(df_group, x=col_cat, y=df_group.columns[1],
                     title=f"{tipo_agreg} de {col_valor} por {col_cat}")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_group)
    else:
        st.info("É preciso ter pelo menos uma coluna categórica e uma numérica para comparações.")

# 4.3 Distribuições
with aba3:
    if numericas:
        col_num = st.selectbox("Escolha a coluna numérica para ver a distribuição", numericas, key="dist_num")
        fig = px.histogram(df, x=col_num, nbins=30, title=f"Distribuição de {col_num}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhuma coluna numérica encontrada para distribuição.")