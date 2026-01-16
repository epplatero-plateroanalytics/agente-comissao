import streamlit as st
import pandas as pd

def aplicar_filtros(df, datas, numericas, categoricas):
    st.subheader("🎛️ Filtros Interativos")

    df_filtrado = df.copy()

    with st.expander("Filtros avançados", expanded=False):

        # Filtros para datas
        if datas:
            st.markdown("### 📅 Filtros de Datas")
            for col in datas:
                try:
                    min_data = df[col].min()
                    max_data = df[col].max()

                    intervalo = st.date_input(
                        f"Intervalo para {col}",
                        value=(min_data, max_data)
                    )

                    if isinstance(intervalo, tuple) and len(intervalo) == 2:
                        inicio, fim = intervalo
                        df_filtrado = df_filtrado[
                            (df_filtrado[col] >= pd.to_datetime(inicio)) &
                            (df_filtrado[col] <= pd.to_datetime(fim))
                        ]
                except:
                    pass

        # Filtros para numéricas
        if numericas:
            st.markdown("### 🔢 Filtros Numéricos")
            for col in numericas:
                minimo = float(df[col].min())
                maximo = float(df[col].max())

                faixa = st.slider(
                    f"Intervalo para {col}",
                    min_value=minimo,
                    max_value=maximo,
                    value=(minimo, maximo)
                )

               