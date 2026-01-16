def gerar_kpis(df, numericas):
    kpis = {}

    for col in numericas:
        kpis[col] = {
            "media": df[col].mean(),
            "min": df[col].min(),
            "max": df[col].max(),
            "soma": df[col].sum()
        }

    return kpis


def gerar_insights(df, datas, numericas, categoricas):
    insights = []

    if numericas:
        insights.append("Os dados numéricos apresentam variação significativa e permitem análises detalhadas.")

    if datas:
        insights.append("A distribuição temporal permite identificar tendências e padrões ao longo do tempo.")

    if categoricas:
        insights.append("As categorias ajudam a segmentar e compreender melhor os dados.")

    return insights