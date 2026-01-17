import streamlit as st
import pandas as pd

def aplicar_filtros(df, colunas_data, colunas_numericas, colunas_categoricas):
    """
    Função atualizada para receber df + listas de colunas
    """
    st.sidebar.header("Filtros Disponíveis")
    
    if df is None or df.empty:
        return df

    df_filtrado = df.copy()

    # 1. Filtros para Colunas Categóricas (Texto)
    # Verifica se a lista não está vazia antes de tentar criar o filtro
    if colunas_categoricas:
        st.sidebar.subheader("Filtrar por Categoria")
        for col in colunas_categoricas:
            # Pega os valores únicos da coluna original
            valores = df[col].unique()
            # Cria o multiselect
            selecionados = st.sidebar.multiselect(f"{col}", options=valores)
            
            # Se o usuário escolher algo, filtra o dataframe
            if selecionados:
                df_filtrado = df_filtrado[df_filtrado[col].isin(selecionados)]

    # 2. Filtros para Colunas Numéricas (Opcional - Slider de Intervalo)
    if colunas_numericas:
        with st.sidebar.expander("Filtros Numéricos"):
            for col in colunas_numericas:
                # Converte para numérico para garantir (ignora erros)
                serie = pd.to_numeric(df[col], errors='coerce')
                if serie.notna().any(): # Só cria se tiver números válidos
                    min_val = float(serie.min())
                    max_val = float(serie.max())
                    
                    # Se min e max forem iguais, não precisa de slider
                    if min_val < max_val:
                        valores = st.slider(f"Faixa de {col}", min_val, max_val, (min_val, max_val))
                        df_filtrado = df_filtrado[
                            (pd.to_numeric(df_filtrado[col], errors='coerce') >= valores[0]) & 
                            (pd.to_numeric(df_filtrado[col], errors='coerce') <= valores[1])
                        ]

    # 3. Retorna o dataframe filtrado para o app.py continuar
    return df_filtrado