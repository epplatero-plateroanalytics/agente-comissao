import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np


# ---------------------------
# KPI CARDS
# ---------------------------
def kpi_cards(df, numericas):
    if not numericas:
        st.info("Nenhuma coluna numérica disponível para KPIs.")
        return

    col = numericas[0]
    serie = df[col].dropna()

    if serie.empty:
        st.info("Coluna numérica vazia após filtros.")
        return

    media = serie.mean()
    mediana = serie.median()
    soma = serie.sum()
    minimo = serie.min()
    maximo = serie.max()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Média", f"{media:,.2f}")
    c2.metric("Mediana", f"{mediana:,.2f}")
    c3.metric("Soma", f"{soma:,.2f}")
    c4.metric("Mínimo", f"{minimo:,.2f}")
    c5.metric("Máximo", f"{maximo:,.2f}")


# ---------------------------
# HISTOGRAMA
# ---------------------------
def grafico_histograma(df, col):
    fig = px.histogram(
        df,
        x=col,
        nbins=30,
        title=f"Distribuição de {col}",
        color_discrete_sequence=["#003366"]
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------
# BOXPLOT
# ---------------------------
def grafico_boxplot(df, col_num, col_cat):
    fig = px.box(
        df,
        x=col_cat,
        y=col_num,
        title=f"Boxplot de {col_num} por {col_cat}",
        color=col_cat,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------
# BARRAS
# ---------------------------
def grafico_barras(df, col_num, col_cat):
    df_bar = df.groupby(col_cat)[col_num].sum().reset_index()

    fig = px.bar(
        df_bar,
        x=col_cat,
        y=col_num,
        title=f"Soma de {col_num} por {col_cat}",
        color=col_cat,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------
# LINHA (SÉRIE TEMPORAL)
# ---------------------------
def grafico_linha(df, col_data, col_valor):
    df_temp = df[[col_data, col_valor]].dropna().sort_values(by=col_data)

    fig = px.line(
        df_temp,
        x=col_data,
        y=col_valor,
        title=f"Evolução de {col_valor} ao longo do tempo",
        markers=True,
        color_discrete_sequence=["#00bcd4"]
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------
# HEATMAP DE CORRELAÇÃO
# ---------------------------
def grafico_heatmap(df, numericas):
    if len(numericas) < 2:
        st.info("É necessário pelo menos 2 colunas numéricas para o heatmap.")
        return

    corr = df[numericas].corr()

    fig = ff.create_annotated_heatmap(
        z=corr.values,
        x=numericas,
        y=numericas,
        colorscale="Blues",
        showscale=True
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------------------------
# TREEMAP
# ---------------------------
def grafico_treemap(df, col_cat, col_num):
    df_tree = df.groupby(col_cat)[col_num].sum().reset_index()

    fig = px.treemap(
        df_tree,
        path=[col_cat],
        values=col_num,
        title=f"Treemap de {col_num} por {col_cat}",
        color=col_num,
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------
# SCATTER MATRIX
# ---------------------------
def grafico_scatter_matrix(df, numericas):
    if len(numericas) < 2:
        st.info("É necessário pelo menos 2 colunas numéricas para scatter matrix.")
        return

    fig = px.scatter_matrix(
        df[numericas],
        dimensions=numericas,
        title="Scatter Matrix (Relações entre variáveis)",
        color_discrete_sequence=["#003366"]
    )
    st.plotly_chart(fig, use_container_width=True)