import pdfkit
import tempfile
import base64
import plotly.io as pio
from insights import resumo_executivo, narrativa_ia
from utils import format_date


# ---------------------------
# CONVERTER FIGURA PLOTLY PARA PNG BASE64
# ---------------------------
def fig_to_base64(fig):
    try:
        png_bytes = pio.to_image(fig, format="png")
        return base64.b64encode(png_bytes).decode("utf-8")
    except Exception:
        return None


# ---------------------------
# GERAR HTML DO PDF
# ---------------------------
def gerar_html_pdf(df, df_filtrado, datas, numericas, categoricas, figs, lang="pt"):
    hoje = format_date(pd.Timestamp.now(), lang)

    # Textos sem acentos
    titulo = "Relatorio Analitico" if lang == "pt" else "Analytical Report"
    marca = "Platero Analytics — Data Intelligence"
    gerado = f"Gerado em {hoje}" if lang == "pt" else f"Generated on {hoje}"
    sumario = "Sumario" if lang == "pt" else "Summary"
    sec1 = "1. Resumo Executivo"
    sec2 = "2. Insights"
    sec3 = "3. Graficos"
    sec4 = "4. Primeiras Linhas"

    # Resumo executivo
    resumo = resumo_executivo(df_filtrado, datas, numericas, categoricas, lang)

    # Narrativa IA
    narrativa = narrativa_ia(df_filtrado, datas, numericas, categoricas, lang)

    # Gráficos convertidos para PNG
    graficos_html = ""
    for fig in figs:
        b64 = fig_to_base64(fig)
        if b64:
            graficos_html += f'<img src="data:image/png;base64,{b64}" style="width:100%; margin-bottom:30px;">'

    # Tabela
    tabela_html = df_filtrado.head().to_html(index=False)

    # Logo vetorial
    logo_svg = """
    <svg width="160" height="100" viewBox="0 0 200 120">
        <rect x="20" y="60" width="25" height="40" fill="#003366"/>
        <rect x="60" y="40" width="25" height="60" fill="#003366"/>
        <rect x="100" y="20" width="25" height="80" fill="#003366"/>
        <circle cx="32" cy="60" r="5" fill="#00bcd4"/>
        <circle cx="72" cy="40" r="5" fill="#00bcd4"/>
        <circle cx="112" cy="20" r="5" fill="#00bcd4"/>
        <line x1="32" y1="60" x2="72" y2="40" stroke="#00bcd4" stroke-width="3"/>
        <line x1="72" y1="40" x2="112" y2="20" stroke="#00bcd4" stroke-width="3"/>
    </svg>
    """

    # HTML completo
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #000; }}
            h1, h2 {{ color: #003366; }}
            .capa {{
                text-align: center;
                margin-top: 150px;
            }}
            .capa h1 {{ font-size: 40px; }}
            .capa h3 {{ color: #555; }}
            .secao {{ margin-top: 40px; }}
            img {{ border: 1px solid #ccc; }}
            table {{
                border-collapse: collapse;
                width: 100%;
                font-size: 12px;
            }}
            table, th, td {{
                border: 1px solid #ccc;
            }}
            th {{
                background-color: #f0f4f8;
            }}
        </style>
    </head>
    <body>

    <!-- CAPA -->
    <div class="capa">
        {logo_svg}
        <h1>{titulo}</h1>
        <h3>{gerado}</h3>
        <h3>{marca}</h3>
    </div>

    <!-- SUMÁRIO -->
    <div class="secao">
        <h2>{sumario}</h2>
        <p>{sec1}</p>
        <p>{sec2}</p>
        <p>{sec3}</p>
        <p>{sec4}</p>
    </div>

    <!-- RESUMO EXECUTIVO -->
    <div class="secao">
        <h2>{sec1}</h2>
        {''.join(f'<p>{p}</p>' for p in resumo)}
    </div>

    <!-- INSIGHTS -->
    <div class="secao">
        <h2>{sec2}</h2>
        {''.join(f'<p>{p}</p>' for p in narrativa)}
    </div>

    <!-- GRÁFICOS -->
    <div class="secao">
        <h2>{sec3}</h2>
        {graficos_html}
    </div>

    <!-- TABELA -->
    <div class="secao">
        <h2>{sec4}</h2>
        {tabela_html}
    </div>

    </body>
    </html>
    """

    return html


# ---------------------------
# GERAR PDF FINAL
# ---------------------------
def gerar_pdf(df, df_filtrado, datas, numericas, categoricas, figs, lang="pt"):
    html = gerar_html_pdf(df, df_filtrado, datas, numericas, categoricas, figs, lang)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
        tmp_html.write(html.encode("utf-8"))
        tmp_html_path = tmp_html.name

    pdf_path = tmp_html_path.replace(".html", ".pdf")

    options = {
        "encoding": "UTF-8",
        "footer-center": "[page]",
        "footer-font-size": "10"
    }

    pdfkit.from_file(tmp_html_path, pdf_path, options=options)

    with open(pdf_path, "rb") as f:
        return f.read()