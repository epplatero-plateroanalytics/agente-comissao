import pandas as pd
from utils import format_date, calcular_outliers, fmt


# ---------------------------
# INSIGHTS NUMÉRICOS
# ---------------------------
def insights_numericos(df, numericas, lang="pt"):
    insights = []

    if not numericas:
        return insights

    for col in numericas:
        serie = df[col].dropna()
        if serie.empty:
            continue

        media = serie.mean()
        mediana = serie.median()
        minimo = serie.min()
        maximo = serie.max()
        desvio = serie.std()

        if lang == "pt":
            insights.append(
                f"Na coluna **{col}**, a média é {fmt(media)}, a mediana é {fmt(mediana)}, "
                f"o valor mínimo é {fmt(minimo)} e o máximo é {fmt(maximo)}. "
                f"O desvio padrão é {fmt(desvio)}, indicando o nível de dispersão."
            )
        else:
            insights.append(
                f"In column **{col}**, the mean is {fmt(media)}, the median is {fmt(mediana)}, "
                f"the minimum value is {fmt(minimo)} and the maximum is {fmt(maximo)}. "
                f"The standard deviation is {fmt(desvio)}, indicating the level of dispersion."
            )

    return insights


# ---------------------------
# INSIGHTS DE DATAS
# ---------------------------
def insights_datas(df, datas, lang="pt"):
    if not datas:
        return []

    col = datas[0]
    serie = df[col].dropna()

    if serie.empty:
        return []

    inicio = serie.min()
    fim = serie.max()

    if lang == "pt":
        return [
            f"O período analisado vai de **{format_date(inicio, 'pt')}** até **{format_date(fim, 'pt')}**."
        ]
    else:
        return [
            f"The analyzed period ranges from **{format_date(inicio, 'en')}** to **{format_date(fim, 'en')}**."
        ]


# ---------------------------
# INSIGHTS DE CATEGORIAS
# ---------------------------
def insights_categorias(df, categoricas, numericas, lang="pt"):
    if not categoricas or not numericas:
        return []

    col_cat = categoricas[0]
    col_num = numericas[0]

    agrupado = (
        df.groupby(col_cat)[col_num]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    if agrupado.empty:
        return []

    if lang == "pt":
        return [
            f"As categorias com maior soma de **{col_num}** são: "
            + ", ".join([f"{i} ({fmt(v)})" for i, v in agrupado.items()])
            + "."
        ]
    else:
        return [
            f"The categories with the highest sum of **{col_num}** are: "
            + ", ".join([f"{i} ({fmt(v)})" for i, v in agrupado.items()])
            + "."
        ]


# ---------------------------
# INSIGHTS DE OUTLIERS
# ---------------------------
def insights_outliers(df, numericas, lang="pt"):
    insights = []

    for col in numericas:
        serie = df[col].dropna()
        if serie.empty:
            continue

        qtd, lim_inf, lim_sup = calcular_outliers(serie)

        if lang == "pt":
            insights.append(
                f"Na coluna **{col}**, foram detectados **{qtd}** possíveis outliers "
                f"pelo método IQR (limites: {fmt(lim_inf)} a {fmt(lim_sup)})."
            )
        else:
            insights.append(
                f"In column **{col}**, **{qtd}** potential outliers were detected "
                f"using the IQR method (limits: {fmt(lim_inf)} to {fmt(lim_sup)})."
            )

    return insights


# ---------------------------
# RESUMO EXECUTIVO (PROFISSIONAL)
# ---------------------------
def resumo_executivo(df, datas, numericas, categoricas, lang="pt"):
    partes = []

    # Introdução
    if lang == "pt":
        partes.append("Este relatório apresenta uma análise detalhada dos dados fornecidos, "
                      "incluindo estatísticas descritivas, comportamento temporal, "
                      "distribuições numéricas, padrões categóricos e detecção de outliers.")
    else:
        partes.append("This report presents a detailed analysis of the provided dataset, "
                      "including descriptive statistics, temporal behavior, "
                      "numeric distributions, categorical patterns, and outlier detection.")

    # Datas
    partes += insights_datas(df, datas, lang)

    # Numéricos
    partes += insights_numericos(df, numericas, lang)

    # Categorias
    partes += insights_categorias(df, categoricas, numericas, lang)

    # Outliers
    partes += insights_outliers(df, numericas, lang)

    return partes


# ---------------------------
# NARRATIVA GERADA POR IA (LOCAL)
# ---------------------------
def narrativa_ia(df, datas, numericas, categoricas, lang="pt"):
    """
    Gera uma narrativa textual inteligente baseada nos dados.
    Não usa modelos externos — é 100% local.
    """

    texto = []

    # Tendências numéricas
    for col in numericas:
        serie = df[col].dropna()
        if serie.empty:
            continue

        tendencia = "estável"
        if serie.iloc[-1] > serie.iloc[0]:
            tendencia = "crescente"
        elif serie.iloc[-1] < serie.iloc[0]:
            tendencia = "decrescente"

        if lang == "pt":
            texto.append(
                f"A variável **{col}** apresenta comportamento **{tendencia}** ao longo do período analisado."
            )
        else:
            texto.append(
                f"The variable **{col}** shows a **{tendencia}** behavior over the analyzed period."
            )

    # Concentração por categoria
    if categoricas and numericas:
        col_cat = categoricas[0]
        col_num = numericas[0]

        agrupado = df.groupby(col_cat)[col_num].sum().sort_values(ascending=False)

        if not agrupado.empty:
            maior = agrupado.index[0]
            valor = agrupado.iloc[0]

            if lang == "pt":
                texto.append(
                    f"A categoria **{maior}** concentra o maior valor total de **{col_num}**, "
                    f"com {fmt(valor)}."
                )
            else:
                texto.append(
                    f"The category **{maior}** concentrates the highest total value of **{col_num}**, "
                    f"with {fmt(valor)}."
                )

    return texto