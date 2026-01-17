import streamlit as st
import pandas as pd

def aplicar_filtros(df):
    st.sidebar.header("Filtros")
    
    # Se o DataFrame estiver vazio, retorna ele mesmo para evitar erros
    if df is None or df.empty:
        return df

    df_filtrado = df.copy()

    # Criação dinâmica de filtros para colunas "Object" (Texto)
    # Você pode personalizar isso, mas aqui está um exemplo genérico seguro
    colunas_texto = df_filtrado.select_dtypes(include=['object']).columns

    for col in colunas_texto:
        # Pega valores únicos para o filtro
        valores = df_filtrado[col].unique()
        
        # Cria o multiselect na barra lateral
        selecionados = st.sidebar.multiselect(f"Filtrar {col}", valores)
        
        # Se o usuário selecionou algo, aplica o filtro
        if selecionados:
            df_filtrado = df_filtrado[df_filtrado[col].isin(selecionados)]

    # --- O PULO DO GATO ESTÁ AQUI EMBAIXO ---
    # O 'return' deve estar alinhado na mesma direção do 'st' e do 'if' lá em cima
    # (Geralmente 4 espaços da margem esquerda)
    return df_filtrado