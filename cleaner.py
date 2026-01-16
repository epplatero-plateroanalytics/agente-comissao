import pandas as pd
import numpy as np

def limpar_planilha(df):
    """
    Limpeza automática universal — versão ULTRA PRO.
    Agora com:
    - Cabeçalho inteligente
    - Conversão numérica robusta
    - Conversão de datas segura (sem falsos positivos)
    - Proteção contra números virarem datas
    """

    # 1. Remover linhas totalmente vazias
    df = df.dropna(how="all")

    # 2. Remover colunas totalmente vazias
    df = df.dropna(axis=1, how="all")

    if df.empty:
        return df

    # ---------------------------------------------------------
    # 3. Detectar automaticamente a linha do cabeçalho real
    # ---------------------------------------------------------
    melhor_linha = 0
    melhor_score = -9999

    for i in range(min(20, len(df))):
        linha = df.iloc[i].astype(str)

        textos = linha.str.contains("[A-Za-z]", regex=True).sum()
        numeros = (
            linha.str.replace(",", ".", regex=False)
                 .str.replace(".", "", regex=False)
                 .str.isnumeric()
                 .sum()
        )

        score = textos - numeros

        if score > melhor_score:
            melhor_score = score
            melhor_linha = i

    # ---------------------------------------------------------
    # 4. Definir cabeçalho real
    # ---------------------------------------------------------
    df.columns = (
        df.iloc[melhor_linha]
        .astype(str)
        .fillna("")
        .str.strip()
    )
    df = df.iloc[melhor_linha + 1 :]

    # 5. Normalizar nomes de colunas
    df.columns = [
        str(c).strip() if c not in ["", None, np.nan] else f"coluna_{i}"
        for i, c in enumerate(df.columns)
    ]

    # 6. Remover "Unnamed"
    df.columns = [
        col if not col.lower().startswith("unnamed") else f"coluna_{i}"
        for i, col in enumerate(df.columns)
    ]

    # ---------------------------------------------------------
    # 7. PRIMEIRO: Converter números com vírgula
    # ---------------------------------------------------------
    for col in df.columns:
        serie = df[col].astype(str)

        # Detectar se a coluna é majoritariamente numérica
        numeric_like = serie.str.replace(".", "", regex=False)\
                            .str.replace(",", ".", regex=False)\
                            .str.match(r"^-?\d+(\.\d+)?$")\
                            .mean()

        # Se mais de 40% dos valores parecem números → tratar como número
        if numeric_like > 0.4:
            df[col] = (
                serie.str.replace(".", "", regex=False)
                     .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------------------------------------------------------
    # 8. DEPOIS: Converter datas (somente se NÃO for numérica)
    # ---------------------------------------------------------
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            continue  # nunca tentar converter números em datas

        serie = df[col].astype(str)

        # Detectar se a coluna parece data
        date_like = serie.str.contains(r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}", regex=True).mean()

        # Só converter se pelo menos 30% dos valores parecem datas
        if date_like > 0.3:
            try:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            except:
                pass

    # 9. Remover linhas vazias
    df = df.dropna(how="all").reset_index(drop=True)

    return df