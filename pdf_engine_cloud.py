from fpdf import FPDF
import plotly.io as pio
import tempfile
import pandas as pd
import unicodedata


# ---------------------------
# FUNÇÃO PARA REMOVER UNICODE
# ---------------------------
def fix_text(text):
    if not isinstance(text, str):
        text = str(text)

    # Normaliza para remover acentos e caracteres especiais
    text = unicodedata.normalize("NFKD", text).encode("latin-1", "ignore").decode("latin-1")

    # Substitui travessões e aspas especiais
    text = text.replace("—", "-").replace("–", "-")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("’", "'").replace("‘", "'")

    return text


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
    pdf.set_font("Arial", "B", 26)
    pdf.cell(0, 20, fix_text("Relatorio Analitico"), ln=True, align="C")

    pdf.set_font("Arial", "", 14)
    hoje = pd.Timestamp.now().strftime("%d/%m/%Y")
    pdf.ln(10)
    pdf.cell(0, 10, fix_text(f"Gerado em {hoje}"), ln=True, align="C")
    pdf.cell(0, 10, fix_text("Platero Analytics - Data Intelligence"), ln=True, align="C")

    # ---------------------------
    # RESUMO EXECUTIVO
    # ---------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, fix_text("1. Resumo Executivo"), ln=True)

    pdf.set_font("Arial", "", 12)
    resumo = [
        "Este relatorio apresenta uma analise completa dos dados enviados.",
        "Inclui metricas, graficos, insights e uma visao geral do comportamento dos dados."
    ]

    for p in resumo:
        pdf.multi_cell(0, 8, fix_text(p))
        pdf.ln(2)

    # ---------------------------
    # GRÁFICOS
    # ---------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, fix_text("2. Graficos"), ln=True)

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
    pdf.cell(0, 10, fix_text("3. Primeiras Linhas da Tabela"), ln=True)

    pdf.set_font("Arial", "", 10)
    tabela = df_filtrado.head().astype(str)

    col_width = pdf.w / (len(tabela.columns) + 1)

    # Cabeçalho
    for col in tabela.columns:
        pdf.cell(col_width, 8, fix_text(col), border=1)
    pdf.ln()

    # Linhas
    for _, row in tabela.iterrows():
        for val in row:
            pdf.cell(col_width, 8, fix_text(str(val)[:20]), border=1)
        pdf.ln()

    # ---------------------------
    # RETORNAR PDF
    # ---------------------------
    return pdf.output(dest="S").encode("latin1")