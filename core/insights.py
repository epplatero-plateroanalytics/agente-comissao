import pandas as pd

# Função 1: Gerar KPIs (que você já tinha, com a correção de números)
def gerar_kpis(df, colunas_numericas):
    kpis = {}
    for col in colunas_numericas:
        if col in df.columns:
            # Converte para numérico forçando erros a virarem NaN
            serie_numerica = pd.to_numeric(df[col], errors='coerce')
            kpis[col] = {
                "soma": serie_numerica.sum(),
                "media": serie_numerica.mean(),
                "max": serie_numerica.max(),
                "min": serie_numerica.min()
            }
    return kpis

# Função 2: Gerar Insights (A QUE ESTÁ FALTANDO)
def gerar_insights(df, analise_coluna="Valor"):
    """
    Gera um resumo simples de texto sobre os dados.
    """
    if df.empty:
        return ["Não há dados suficientes para gerar insights."]
    
    insights = []
    
    # Exemplo de insight: Qual o item mais frequente em uma coluna de texto?
    # Pega a primeira coluna de texto que encontrar (exceto data)
    colunas_texto = df.select_dtypes(include=['object']).columns
    if len(colunas_texto) > 0:
        col_top = colunas_texto[0]
        top_item = df[col_top].mode()[0]
        insights.append(f"O item mais frequente em '{col_top}' é: {top_item}")
    
    # Exemplo de insight: Total geral (se houver coluna de valor)
    if analise_coluna in df.columns:
         total = pd.to_numeric(df[analise_coluna], errors='coerce').sum()
         insights.append(f"O valor total acumulado é de {total:,.2f}")

    return insights