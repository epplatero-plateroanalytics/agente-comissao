import pandas as pd
import numpy as np

def limpar_planilha(df):
    """
    Limpeza universal — versão TITANIUM.
    - Remove objetos e converte tudo para string antes de qualquer .str
    - Cabeçalho inteligente
    - Conversão numérica segura
    - Conversão de datas segura
    """

    # 1. Remover linhas totalmente vazias
    df = df.dropna(how="all")

    # 2. Remover colunas totalmente vazias
    df = df.dropna(axis=1, how="all")

    if df.empty:
        return df

    # ---------------------------------------------------------
    # 3. Converter absolutamente TUDO para string imediatamente
    # ---------------------------------------------------------
    df = df.astype(str)

    # ---------------------------------------------------------
    # 4. Detectar automaticamente a linha do cabeçalho real
    # ---------------------------------------------------------
    melhor_linha = 0
    melhor_score = -9999

    for i in range(min(20, len(df))):
        linha = df.iloc[i]

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
    # 5. Definir cabeçalho real
    # ---------------------------------------------------------
    df.columns = (
        df.iloc[melhor_linha]
        .astype(str)
        .fillna("")
        .str.strip()
    )
    df = df.iloc[melhor_linha + 1 :]

    # 6. Normalizar nomes de colunas
    df.columns = [
        str(c).strip() if c not in ["", None, np.nan] else f"coluna_{i}"
        for i, c in enumerate(df.columns)
    ]

    # 7. Remover "Unnamed"
    df.columns = [
        col if not col.lower().startswith("unnamed") else f"coluna_{i}"
        for i, col in enumerate(df.columns)
    ]

    # ---------------------------------------------------------
    # 8. Converter tudo para string novamente (garantia)
    # ---------------------------------------------------------
    for col in df.columns:
        df[col] = df[col].astype(str)

    # ---------------------------------------------------------
    # 9. Converter números com vírgula (somente se parecer número)
    # ---------------------------------------------------------
    for col in df.columns:
        serie = df[col]

        numeric_like = (
            serie.str.replace(".", "", regex=False)
                 .str.replace(",", ".", regex=False)
                 .str.match(r"^-?\d+(\.\d+)?$")
                 .mean()
        )

        if numeric_like > 0.4:
            df[col] = (
                serie.str.replace(".", "", regex=False)
                     .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------------------------------------------------------
    # 10. Converter datas (somente se NÃO for numérica)
    # ---------------------------------------------------------
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            continue

        serie = df[col]

        date_like = serie.str.contains(
            r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}",
            regex=True
        ).mean()

        if date_like > 0.3:
            try:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            except:
                pass

    # 11. Remover linhas vazias
    df = df.dropna(how="all").reset_index(drop=True)

    return df