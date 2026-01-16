import pandas as pd
import numpy as np

def limpar_planilha(df):
    """
    Limpeza automática universal — versão PRO FINAL.
    Corrige:
    - Cabeçalho na linha errada
    - Colunas Unnamed
    - Colunas vazias
    - Linhas lixo
    - Números com vírgula (convertidos ANTES das datas)
    - Datas
    - Nomes inválidos de colunas
    """

    # 1. Remover linhas totalmente vazias
    df = df.dropna(how="all")

    # 2. Remover colunas totalmente vazias
    df = df.dropna(axis=1, how="all")

    if df.empty:
        return df

    # ---------------------------------------------------------
    # 3. Detectar automaticamente a linha do cabeçalho real (versão PRO)
    # ---------------------------------------------------------
    melhor_linha = 0
    melhor_score = -9999

    for i in range(min(15, len(df))):
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

    # 5. Garantir que todos os nomes de colunas são strings válidas
    df.columns = [
        str(c).strip() if c not in [None, np.nan, "nan", "None", ""] else f"coluna_{i}"
        for i, c in enumerate(df.columns)
    ]

    # 6. Remover colunas Unnamed
    df.columns = [
        col if not col.lower().startswith("unnamed") else f"coluna_{i}"
        for i, col in enumerate(df.columns)
    ]

    # 7. Limpar caracteres estranhos
    df.columns = (
        pd.Series(df.columns)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace("  ", " ", regex=False)
        .str.strip()
        .tolist()
    )

    # ---------------------------------------------------------
    # 8. PRIMEIRO: Converter números com vírgula (ANTES das datas)
    # ---------------------------------------------------------
    for col in df.columns:
        try:
            if df[col].dtype == object:
                s = df[col].astype(str)

                # remover separador de milhar
                s = s.str.replace(".", "", regex=False)

                # trocar vírgula por ponto
                s = s.str.replace(",", ".", regex=False)

                df[col] = pd.to_numeric(s, errors="ignore")
        except:
            pass

    # ---------------------------------------------------------
    # 9. DEPOIS: Converter datas automaticamente
    # ---------------------------------------------------------
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="raise")
        except:
            pass

    # 10. Remover linhas vazias após limpeza
    df = df.dropna(how="all").reset_index(drop=True)

    return df