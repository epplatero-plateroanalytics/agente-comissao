from fpdf import FPDF
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd


# ---------------------------------------------------------
#  Função auxiliar: converter imagem matplotlib → base64
# ---------------------------------------------------------
def fig_to_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=200, bbox_inches="tight")
    buffer.seek(0)
    img_bytes = buffer.read()
    return base64.b64encode(img_bytes).decode("utf-8")


# ---------------------------------------------------------
#  Classe PDF Premium Signature
# ---------------------------------------------------------
class PDFPremium(FPDF):

    def header(self):
        pass  # capa e sumário são criados manualmente

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "Platero Analytics — Relatório Premium", 0, 0, "C")


# ---------------------------------------------------------
#  Função principal: gerar PDF
# ---------------------------------------------------------
def gerar_pdf(df, df_filtrado, datas, numericas, categoricas, kpis, insights):

    pdf = PDFPremium()
    pdf.set_auto_page_break(auto=True, margin=15)

    # -----------------------------------------------------
    #  CAPA PREMIUM
    # -----------------------------------------------------
    pdf.add_page()

    # Faixa azul
    pdf.set_fill_color(10, 26, 47)  # azul escuro
    pdf.rect(0, 0, 210, 60, "F")

    # Faixa dourada
    pdf.set_fill_color(212, 175, 55)
    pdf.rect(0, 60, 210, 5, "F")

    # Logo
    try:
        pdf.image("pdf/assets/logo.png", x=70, y=75, w=70)
    except:
        pass

    pdf.set_xy(10, 140)
    pdf.set_font("Arial", "B", 28)
    pdf.set_text_color(10, 26, 47)
    pdf.cell(0, 15, "Relatório Premium", 0, 1, "C")

    pdf.set_font("Arial", "", 16)
    pdf.cell(0, 10, "Platero Analytics — Data Intelligence", 0, 1, "C")

    pdf.ln(20)

    # -----------------------------------------------------
    #  SUMÁRIO
    # -----------------------------------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(10, 26, 47)
    pdf.cell(0, 10, "Sumário", 0, 1)

    pdf.set_font("Arial", "", 14)
    pdf.ln(5)
    pdf.cell(0, 8, "1. KPIs", 0, 1)
    pdf.cell(0, 8, "2. Insights", 0, 1)
    pdf.cell(0, 8, "3. Gráficos", 0, 1)
    pdf.cell(0, 8, "4. Tabela de Dados", 0, 1)
    pdf.cell(0, 8, "5. Agradecimento", 0, 1)

    # -----------------------------------------------------
    #  SEÇÃO 1 — KPIs
    # -----------------------------------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "1. KPIs", 0, 1)

    pdf.set_font("Arial", "", 12)

    for col, valores in kpis.items():
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, f"{col}", 0, 1)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 6, f"Média: {valores['media']:.2f}", 0, 1)
        pdf.cell(0, 6, f"Mínimo: {valores['min']}", 0, 1)
        pdf.cell(0, 6, f"Máximo: {valores['max']}", 0, 1)
        pdf.cell(0, 6, f"Soma: {valores['soma']:.2f}", 0, 1)

    # -----------------------------------------------------
    #  SEÇÃO 2 — INSIGHTS
    # -----------------------------------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "2. Insights", 0, 1)

    pdf.set_font("Arial", "", 12)
    for texto in insights:
        pdf.multi_cell(0, 8, f"- {texto}")
        pdf.ln(2)

    # -----------------------------------------------------
    #  SEÇÃO 3 — GRÁFICOS
    # -----------------------------------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "3. Gráficos", 0, 1)

    if numericas:
        for col in numericas:
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(df_filtrado[col], color="#0A1A2F")
            ax.set_title(f"Evolução de {col}")
            ax.grid(True, alpha=0.3)

            img_b64 = fig_to_base64(fig)
            plt.close(fig)

            pdf.ln(5)
            pdf.image(BytesIO(base64.b64decode(img_b64)), w=180)

    # -----------------------------------------------------
    #  SEÇÃO 4 — TABELA
    # -----------------------------------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "4. Tabela de Dados", 0, 1)

    pdf.set_font("Arial", "", 10)

    colunas = df_filtrado.columns.tolist()
    largura = 190 / len(colunas)

    for col in colunas:
        pdf.cell(largura, 8, str(col), 1, 0, "C")
    pdf.ln()

    for _, linha in df_filtrado.iterrows():
        for col in colunas:
            pdf.cell(largura, 6, str(linha[col])[:20], 1, 0, "C")
        pdf.ln()

    # -----------------------------------------------------
    #  SEÇÃO 5 — AGRADECIMENTO
    # -----------------------------------------------------
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(10, 26, 47)
    pdf.cell(0, 20, "Obrigado!", 0, 1, "C")

    pdf.set_font("Arial", "", 14)
    pdf.cell(0, 10, "A Platero Analytics agradece sua confiança.", 0, 1, "C")

    pdf.ln(20)
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, "Assinatura Digital:", 0, 1)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Platero Analytics", 0, 1)

    # -----------------------------------------------------
    #  EXPORTAR PDF
    # -----------------------------------------------------
    return pdf.output(dest="S").encode("latin-1")