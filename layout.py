import streamlit as st
from charts import (
    kpi_cards,
    grafico_histograma,
    grafico_boxplot,
    grafico_barras,
    grafico_linha,
    grafico_heatmap,
    grafico_treemap,
    grafico_scatter_matrix
)
from insights import insights_numericos, insights_datas, insights_categorias, insights_outliers
from filters import aplicar_filtros


# ---------------------------
# LAYOUT PRINCIPAL COM ABAS
# ---------------------------
def render_layout(df, datas, numericas, categoricas, lang="pt"):
    st.title("Agente Universal PRO — Platero Analytics")

    # Sidebar com filtros
    df_filtrado = aplicar_filtros(df, datas, categoricas, numericas, lang)

    # Abas principais
    aba1, aba2, aba3, aba4 = st.tabs([
        "📊 Visão Geral",
        "📈 Gráficos",
        "🧠 Insights",
        "📄 PDF"
    ])

    # ---------------------------
    # ABA 1 — VISÃO GERAL
    # ---------------------------
    with aba1:
        st.header("📊 Visão Geral dos Dados")

        st.subheader("Prévia dos Dados")
        st.dataframe(df_filtrado.head())

        st.subheader("KPIs")
        kpi_cards(df_filtrado, numericas)

        st.subheader("Tipos de Colunas")
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Datas:** {datas if datas else '-'}")
        c2.write(f"**Numéricas:** {numericas if numericas else '-'}")
        c3.write(f"**Categóricas:** {categoricas if categoricas else '-'}")

    # ---------------------------
    # ABA 2 — GRÁFICOS
    # ---------------------------
    with aba2:
        st.header("📈 Gráficos Interativos")

        figs = []  # armazenar figuras para PDF

        if numericas:
            col_num = st.selectbox("Selecione uma coluna numérica", numericas)

            st.subheader("Histograma")
            fig1 = grafico_histograma(df_filtrado, col_num)
            figs.append(fig1)

            if categoricas:
                col_cat = categoricas[0]

                st.subheader("Boxplot")
                fig2 = grafico_boxplot(df_filtrado, col_num, col_cat)
                figs.append(fig2)

                st.subheader("Barras")
                fig3 = grafico_barras(df_filtrado, col_num, col_cat)
                figs.append(fig3)

        if datas and numericas:
            col_data = datas[0]
            col_val = numericas[0]

            st.subheader("Linha (Série Temporal)")
            fig4 = grafico_linha(df_filtrado, col_data, col_val)
            figs.append(fig4)

        if numericas and len(numericas) > 1:
            st.subheader("Heatmap de Correlação")
            fig5 = grafico_heatmap(df_filtrado, numericas)
            figs.append(fig5)

            st.subheader("Scatter Matrix")
            fig6 = grafico_scatter_matrix(df_filtrado, numericas)
            figs.append(fig6)

        if categoricas and numericas:
            st.subheader("Treemap")
            fig7 = grafico_treemap(df_filtrado, categoricas[0], numericas[0])
            figs.append(fig7)

        st.session_state["figs_pdf"] = figs

    # ---------------------------
    # ABA 3 — INSIGHTS
    # ---------------------------
    with aba3:
        st.header("🧠 Insights Automáticos")

        st.subheader("Numéricos")
        for i in insights_numericos(df_filtrado, numericas, lang):
            st.write("- " + i)

        st.subheader("Datas")
        for i in insights_datas(df_filtrado, datas, lang):
            st.write("- " + i)

        st.subheader("Categorias")
        for i in insights_categorias(df_filtrado, categoricas, numericas, lang):
            st.write("- " + i)

        st.subheader("Outliers")
        for i in insights_outliers(df_filtrado, numericas, lang):
            st.write("- " + i)

    # ---------------------------
    # ABA 4 — PDF
    # ---------------------------
    with aba4:
        st.header("📄 Gerar PDF Profissional")

        st.write("Clique no botão abaixo para gerar o PDF com gráficos, insights e resumo executivo.")

        if st.button("Gerar PDF"):
            st.session_state["pdf_ready"] = True

        return df_filtrado