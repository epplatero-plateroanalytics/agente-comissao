import pandas as pd
import numpy as np


# ---------------------------
# FORMATAR DATA POR IDIOMA
# ---------------------------
def format_date(dt, lang="pt"):
    if pd.isna(dt):
        return ""
    if lang == "pt":
        return dt.strftime("%d/%m/%Y")
    return dt.strftime("%b %d, %Y")


# ---------------------------
# DETECTAR TIPOS DE COLUNAS
# ---------------------------
def detectar_tipos(df):
    datas = []
    numericas = []
    categoricas = []

    for col in df.columns:
        serie = df[col]

        # Datas
        if pd.api.types.is_datetime64_any_dtype(serie):
            datas.append(col)
            continue

        # Numéricas
        if pd.api.types.is_numeric_dtype(serie):
            numericas.append(col)
            continue

        # Categóricas
        if pd.api.types.is_string_dtype(serie) or pd.api.types.is_object_dtype(serie):
            categoricas.append(col)
            continue

    return datas, numericas, categoricas


# ---------------------------
# VALIDAR SE DATAFRAME ESTÁ VAZIO
# ---------------------------
def df_vazio(df):
    return df is None or df.empty or len(df.columns) == 0


# ---------------------------
# CONVERTER SÉRIE PARA FLOAT (SEGURA)
# ---------------------------
def to_float_safe(series):
    try:
        s = series.astype(str)
        s = s.str.replace(".", "", regex=False)
        s = s.str.replace(",", ".", regex=False)
        return pd.to_numeric(s, errors="coerce")
    except:
        return series


# ---------------------------
# CALCULAR OUTLIERS (IQR)
# ---------------------------
def calcular_outliers(series):
    serie = series.dropna()
    if serie.empty:
        return 0, None, None

    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1

    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr

    qtd = serie[(serie < lim_inf) | (serie > lim_sup)].shape[0]

    return qtd, lim_inf, lim_sup


# ---------------------------
# FORMATAR NÚMERO COM 2 CASAS
# ---------------------------
def fmt(x):
    try:
        return f"{x:,.2f}"
    except:
        return x