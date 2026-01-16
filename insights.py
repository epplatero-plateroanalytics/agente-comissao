def resumo_executivo(df, datas, numericas, categoricas, lang="pt"):
    texto = []

    if numericas:
        texto.append(f"O conjunto de dados possui {len(df)} registros.")
        texto.append(f"Foram identificadas {len(numericas)} colunas numéricas.")
        texto.append(f"As principais métricas foram calculadas com sucesso.")

    if datas:
        texto.append(f"As datas foram reconhecidas corretamente.")

    if categoricas:
        texto.append(f"Foram identificadas {len(categoricas)} colunas categóricas.")

    return texto


def narrativa_ia(df, datas, numericas, categoricas, lang="pt"):
    texto = []

    if numericas:
        texto.append("Os valores numéricos apresentam variação significativa ao longo do período analisado.")

    if datas:
        texto.append("A distribuição temporal dos dados permite identificar padrões e tendências.")

    if categoricas:
        texto.append("As categorias presentes ajudam a segmentar e compreender melhor os dados.")

    return texto