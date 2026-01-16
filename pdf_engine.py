from fpdf import FPDF
import plotly.io as pio
import tempfile
import pandas as pd
from insights import resumo_executivo, narrativa_ia
from utils import format_date


# ---------------------------
# CONVERTER FIGURA PLOTLY PARA PNG TEMPORÁRIO
# ---------------------------
def fig_to_png(fig):
    try:
        png_bytes = pio.to_image(fig, format="png")
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp.write(png_bytes)
        tmp.close()
        return tmp.name
    except:
        return None


# ---------------------------
# GERAR PDF (COMPATÍVEL COM STREAMLIT CLOUD)
# ---------------------------
def gerar_pdf(df, df_filtrado, datas, numericas, categoricas, figs, lang="pt"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---------------------------
    # CAPA
    # ---------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 28)
    pdf.cell(0, 20, "Relatório Analítico", ln=True, align="C")

    pdf.set_font("Arial", "", 14)
    hoje = format_date(pd.Timestamp.now(), lang)
    pdf.ln(10)
    pdf.cell(0, 10, f"Gerado em {hoje}", ln=True, align="C")
    pdf.cell(0, 10, "Platero Analytics — Data Intelligence", ln=True, align="C")

    # ---------------------------
    # RESUMO EXECUTIVO
    # ---------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "1. Resumo Executivo", ln=True)

    pdf.set_font("Arial", "", 12)
    resumo = resumo_executivo(df_filtrado, datas, numericas, categoricas, lang)
    for p in resumo:
        pdf.multi_cell(0, 8, p)
        pdf.ln(2)

    # ---------------------------
    # INSIGHTS
    # ---------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "2. Insights", ln=True)

    pdf.set_font("Arial", "", 12)
    narrativa = narrativa_ia(df_filtrado, datas, numericas, categoricas, lang)
    for p in narrativa:
        pdf.multi_cell(0, 8, p)
        pdf.ln(2)

    # ---------------------------
    # GRÁFICOS
    # ---------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "3. Gráficos", ln=True)

    for fig in figs:
        path = fig_to_png(fig)
        if path:
            pdf.ln(5)
            pdf.image(path, w=180)

    # ---------------------------
    # TABELA (primeiras linhas)
    # ---------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "4. Primeiras Linhas", ln=True)

    pdf.set_font("Arial", "", 10)
    tabela = df_filtrado.head().astype(str)

    col_width = pdf.w / (len(tabela.columns) + 1)

    # Cabeçalho
    for col in tabela.columns:
        pdf.cell(col_width, 8, col, border=1)
    pdf.ln()

    # Linhas
    for _, row in tabela.iterrows():
        for val in row:
            pdf.cell(col_width, 8, str(val)[:20], border=1)
        pdf.ln()

    # ---------------------------
    # RETORNAR PDF
    # ---------------------------
    return pdf.output(dest="S").encode("latin1")