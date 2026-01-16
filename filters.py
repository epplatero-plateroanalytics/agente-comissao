import streamlit as st
import pandas as pd
from utils import calcular_outliers


# ---------------------------
# FILTRO DE DATAS
# ---------------------------
def filtro_datas(df, datas, lang="pt"):
    if not datas:
        return df

    col_data = datas[0]

    serie = df[col_data].dropna()
    if serie.empty:
        return df

    min_date = serie.min().date()
    max_date = serie.max().date()

    st.sidebar.subheader("📅 Intervalo de Datas")

    intervalo = st.sidebar.date_input(
        "Selecione o intervalo",
        value=(min_date, max_date)
    )

    if isinstance(intervalo, tuple) and len(intervalo) == 2:
        inicio, fim = intervalo
        df = df[
            (df[col_data] >= pd.to_datetime(inicio)) &
            (df[col_data] <= pd.to_datetime(fim))
        ]

    return df


# ---------------------------
# FILTRO DE CATEGORIAS
# ---------------------------
def filtro_categorias(df, categoricas, lang="pt"):
    if not categoricas:
        return df

    col_cat = categoricas[0]

    st.sidebar.subheader("🏷️ Filtro de Categorias")

    valores = sorted(df[col_cat].dropna().astype(str).unique().tolist())

    selecionados = st.sidebar.multiselect(
        f"Valores em {col_cat}",
        options=valores,
        default=valores
    )

    modo = st.sidebar.selectbox(
        "Modo de filtro",
        ["Contém", "Começa com", "Igual a"]
    )

    if selecionados:
        mask = False
        for v in selecionados:
            if modo == "Contém":
                mask = mask | df[col_cat].astype(str).str.contains(v, case=False, na=False)
            elif modo == "Começa com":
                mask = mask | df[col_cat].astype(str).str.startswith(v, na=False)
            else:
                mask = mask | (df[col_cat].astype(str) == v)

        df = df[mask]

    return df


# ---------------------------
# FILTRO NUMÉRICO
# ---------------------------
def filtro_numerico(df, numericas, lang="pt"):
    if not numericas:
        return df

    col_num = numericas[0]

    st.sidebar.subheader("🔢 Filtro Numérico")

    serie = df[col_num].dropna()
    if serie.empty:
        return df

    min_val = float(serie.min())
    max_val = float(serie.max())

    intervalo = st.sidebar.slider(
        f"Intervalo de {col_num}",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val)
    )

    df = df[(df[col_num] >= intervalo[0]) & (df[col_num] <= intervalo[1])]

    # Remover outliers
    remover = st.sidebar.checkbox("Remover outliers (IQR)")
    if remover:
        qtd, lim_inf, lim_sup = calcular_outliers(serie)
        df = df[(df[col_num] >= lim_inf) & (df[col_num] <= lim_sup)]

    return df


# ---------------------------
# APLICAÇÃO COMPLETA DOS FILTROS
# ---------------------------
def aplicar_filtros(df, datas, categoricas, numericas, lang="pt"):
    st.sidebar.title("🔍 Filtros Avançados")

    df_f = df.copy()

    df_f = filtro_datas(df_f, datas, lang)
    df_f = filtro_categorias(df_f, categoricas, lang)
    df_f = filtro_numerico(df_f, numericas, lang)

    st.sidebar.markdown("---")
    st.sidebar.write(f"**Linhas após filtros:** {len(df_f)}")

    return df_f