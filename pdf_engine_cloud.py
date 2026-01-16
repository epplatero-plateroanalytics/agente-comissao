from fpdf import FPDF
import plotly.io as pio
import tempfile
import pandas as pd
import unicodedata
from insights import resumo_executivo, narrativa_ia


def fix_text(text):
    if not isinstance(text, str):
        text = str(text)
    text = unicodedata.normalize("NFKD", text).encode("latin-1", "ignore").decode("latin-1")
    return text


def fig_to_png(fig):
    try:
        png_bytes = pio.to_image(fig, format="png")
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp.write(png_bytes)
        tmp.close()
        return tmp.name
    except:
        return None


def gerar_pdf(df, df_filtrado, datas, numericas, categoricas, figs, lang="pt"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Arial", "B", 28)
    pdf.cell(0, 20, fix_text("Relatorio Premium"), ln=True, align="C")

    pdf.set_font("Arial", "", 16)
    pdf.cell(0, 10, fix_text("Analise Completa dos Dados"), ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, fix_text(f"Gerado em {pd.Timestamp.now().strftime('%d/%m/%Y')}"), ln=True, align="C")

    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, fix_text("1. Resumo Executivo"), ln=True)

    pdf.set_font("Arial", "", 12)
    resumo = resumo_executivo(df_filtrado, datas, numericas, categoricas, lang)
    for p in resumo:
        pdf.multi_cell(0, 8, fix_text(p))
        pdf.ln(2)

    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, fix_text("2. Insights"), ln=True)

    pdf.set_font("Arial", "", 12)
    narrativa = narrativa_ia(df_filtrado, datas, numericas, categoricas, lang)
    for p in narrativa:
        pdf.multi_cell(0, 8, fix_text(p))
        pdf.ln(2)

    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, fix_text("3. Graficos"), ln=True)

    for fig in figs:
        path = fig_to_png(fig)
        if path:
            pdf.ln(5)
            pdf.image(path, w=180)

    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, fix_text("4. Primeiras Linhas da Tabela"), ln=True)

    pdf.set_font("Arial", "", 10)
    tabela = df_filtrado.head().astype(str)
    col_width = pdf.w / (len(tabela.columns) + 1)

    for col in tabela.columns:
        pdf.cell(col_width, 8, fix_text(col), border=1)
    pdf.ln()

    for _, row in tabela.iterrows():
        for val in row:
            pdf.cell(col_width, 8, fix_text(str(val)[:20]), border=1)
        pdf.ln()

    return bytes(pdf.output(dest="S"))