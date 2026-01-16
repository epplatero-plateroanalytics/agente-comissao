import pandas as pd
import numpy as np
import re

def limpar_planilha(df):
    """
    Limpeza universal — versão ABSOLUTA (sem .str)
    - Cabeçalho inteligente
    - Conversão numérica segura
    - Conversão de datas segura
    - Nenhum uso de .str (evita todos os erros)
    """

    # 1. Remover linhas totalmente vazias
    df = df.dropna(how="all")

    # 2. Remover colunas totalmente vazias
    df = df.dropna(axis=1, how="all")

    if df.empty:
        return df

    # ---------------------------------------------------------
    # 3. Converter tudo para string de forma segura
    # ---------------------------------------------------------
    df = df.applymap(lambda x: "" if pd.isna(x) else str(x))

    # ---------------------------------------------------------
    # 4. Detectar automaticamente a linha do cabeçalho real
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # 5. Definir cabeçalho real
    # ---------------------------------------------------------
    df.columns = [c.strip() for c in df.iloc[melhor_linha].tolist()]
    df = df.iloc[melhor_linha + 1 :]

    # 6. Normalizar nomes de colunas
    df.columns = [
        c if c not in ["", None, np.nan] else f"coluna_{i}"
        for i, c in enumerate(df.columns)
    ]

    # 7. Remover "Unnamed"
    df.columns = [
        col if not col.lower().startswith("unnamed") else f"coluna_{i}"
        for i, col in enumerate(df.columns)
    ]

    # ---------------------------------------------------------
    # 8. Converter números (sem .str)
    # ---------------------------------------------------------
    for col in df.columns:
        def parse_num(x):
            x = x.replace(".", "").replace(",", ".")
            return pd.to_numeric(x, errors="coerce")

        # Detectar se a coluna é majoritariamente numérica
        numeric_like = sum(
            1 for v in df[col] if re.fullmatch(r"-?\d+([.,]\d+)?", v)
        ) / len(df[col])

        if numeric_like > 0.4:
            df[col] = df[col].apply(parse_num)

    # ---------------------------------------------------------
    # 9. Converter datas (sem .str)
    # ---------------------------------------------------------
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            continue

        date_like = sum(
            1 for v in df[col] if re.search(r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}", v)
        ) / len(df[col])

        if date_like > 0.3:
            try:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            except:
                pass

    # 10. Remover linhas vazias
    df = df.dropna(how="all").reset_index(drop=True)

    return df