import pandas as pd
import numpy as np
import re

def limpar_planilha(df):
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    if df.empty:
        return df

    df = df.applymap(lambda x: "" if pd.isna(x) else str(x))

    melhor_linha = 0
    melhor_score = -9999

    for i in range(min(20, len(df))):
        linha = df.iloc[i].tolist()
        textos = sum(1 for v in linha if re.search(r"[A-Za-z]", v))
        numeros = sum(1 for v in linha if re.fullmatch(r"-?\d+([.,]\d+)?", v))
        score = textos - numeros
        if score > melhor_score:
            melhor_score = score
            melhor_linha = i

    df.columns = [c.strip() for c in df.iloc[melhor_linha].tolist()]
    df = df.iloc[melhor_linha + 1:]

    df.columns = [
        c if c not in ["", None, np.nan] else f"coluna_{i}"
        for i, c in enumerate(df.columns)
    ]

    df.columns = [
        col if not col.lower().startswith("unnamed") else f"coluna_{i}"
        for i, col in enumerate(df.columns)
    ]

    for col in df.columns:
        serie = df[col]
        numeric_like = sum(
            1 for v in serie if re.fullmatch(r"-?\d+([.,]\d+)?", v)
        ) / len(serie)

        if numeric_like > 0.4:
            df[col] = df[col].apply(
                lambda x: pd.to_numeric(
                    x.replace(".", "").replace(",", "."),
                    errors="coerce"
                )
            )

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            continue

        serie = df[col]
        date_like = sum(
            1 for v in serie if re.search(r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}", v)
        ) / len(serie)

        if date_like > 0.3:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    df = df.dropna(how="all").reset_index(drop=True)
    return df