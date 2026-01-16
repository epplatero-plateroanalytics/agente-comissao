import streamlit as st
import plotly.express as px

def salvar_figura(fig):
    if "figs_pdf" not in st.session_state:
        st.session_state["figs_pdf"] = []
    st.session_state["figs_pdf"].append(fig)


def render_layout(df, datas, numericas, categoricas, lang="pt"):
    abas = st.tabs(["📊 Visão Geral", "📈 Gráficos", "🧠 Insights", "📄 PDF"])

    with abas[0]:
        st.subheader("Prévia dos Dados")
        st.dataframe(df.head())

        st.subheader("KPIs")
        if numericas:
            for col in numericas:
                st.metric(f"Média de {col}", f"{df[col].mean():,.2f}")
        else:
            st.info("Nenhuma coluna numérica disponível.")

    with abas[1]:
        st.subheader("Gráficos Automáticos")

        if numericas and categoricas:
            col_num = numericas[0]
            col_cat = categoricas[0]

            fig = px.bar(df, x=col_cat, y=col_num)
            st.plotly_chart(fig, use_container_width=True)
            salvar_figura(fig)

        else:
            st.info("Não há dados suficientes para gráficos.")

    with abas[2]:
        st.subheader("Insights Automáticos")
        st.write("Insights serão incluídos no PDF.")

    with abas[3]:
        if st.button("Gerar Relatório Premium"):
            st.session_state["pdf_ready"] = True
            st.success("Gerando PDF...")

    return df