import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pdfkit
import tempfile
from datetime import datetime

st.set_page_config(page_title="Universal Analytics Agent", layout="wide")

# ---------------------------
# TEXTOS BILÍNGUES (INTERFACE)
# ---------------------------
T = {
    "pt": {
        "app_title": "Agente Universal de Planilhas – Versão Premium",
        "app_subtitle": "Envie uma planilha e gere análises avançadas, insights e relatório em PDF.",
        "language_label": "🌐 Idioma",
        "lang_pt": "Português",
        "lang_en": "Inglês",
        "upload_label": "Selecione um arquivo",
        "upload_hint": "Envie uma planilha para começar.",
        "error_read": "Erro ao ler o arquivo.",
        "error_empty": "A planilha está vazia.",
        "warn_dup_cols": "Colunas duplicadas detectadas. Renomeando automaticamente.",
        "preview_title": "Prévia dos dados",
        "types_title": "Tipos de colunas detectados",
        "num_cols": "Numéricas",
        "date_cols": "Datas",
        "cat_cols": "Categóricas",
        "filters_title": "Filtros avançados",
        "filter_date_range": "Intervalo de datas",
        "filter_category": "Categoria",
        "filter_category_mode": "Modo de filtro de texto",
        "filter_contains": "Contém",
        "filter_starts": "Começa com",
        "filter_equals": "Igual a",
        "filter_numeric": "Filtro numérico",
        "filter_numeric_col": "Coluna numérica",
        "filter_numeric_range": "Intervalo de valores",
        "filter_outliers": "Remover outliers (IQR)",
        "insights_title": "🧠 Insights automáticos e estatística descritiva",
        "stats_title": "Estatísticas descritivas",
        "corr_title": "Matriz de correlação entre variáveis numéricas",
        "top_cat_title": "Top 5 categorias em {cat} por soma de {val}",
        "insights_list_title": "Insights em linguagem natural",
        "outliers_title": "Outliers (método IQR)",
        "no_num_cols": "Não há colunas numéricas suficientes para estatísticas descritivas.",
        "no_outliers_info": "Não foi possível calcular outliers.",
        "viz_title": "📊 Visualizações",
        "select_num_col": "Selecione uma coluna numérica para análise detalhada",
        "hist_title": "Distribuição de {col}",
        "box_title": "Boxplot de {col} por {cat}",
        "bar_title": "Soma de {col} por {cat}",
        "line_title": "Evolução de {col} ao longo do tempo",
        "pdf_title_section": "📄 Gerar relatório PDF (Layout Profissional)",
        "pdf_button": "Gerar PDF",
        "pdf_success": "PDF gerado com sucesso!",
        "pdf_download": "Baixar PDF",
        "insight_num": "Em {col}, a média é {mean:,.2f}, mediana {median:,.2f}, desvio padrão {std:,.2f}, mínimo {min:,.2f} e máximo {max:,.2f}.",
        "insight_period": "O período analisado vai de {start} até {end}.",
        "insight_topcat": "As 5 principais categorias em {cat}, considerando a soma de {val}, foram calculadas para destacar concentrações.",
        "insight_corr": "Foi calculada a correlação entre as variáveis numéricas para identificar relações lineares.",
        "insight_outliers": "Em {col}, foram detectados {qtd} possíveis outliers usando o método IQR."
    },

    "en": {
        "app_title": "Universal Spreadsheet Agent – Premium Version",
        "app_subtitle": "Upload a spreadsheet and generate advanced analysis, insights, and a professional PDF report.",
        "language_label": "🌐 Language",
        "lang_pt": "Portuguese",
        "lang_en": "English",
        "upload_label": "Select a file",
        "upload_hint": "Upload a spreadsheet to begin.",
        "error_read": "Error reading the file.",
        "error_empty": "The spreadsheet is empty.",
        "warn_dup_cols": "Duplicate columns detected. Renaming automatically.",
        "preview_title": "Data preview",
        "types_title": "Detected column types",
        "num_cols": "Numeric",
        "date_cols": "Date",
        "cat_cols": "Categorical",
        "filters_title": "Advanced filters",
        "filter_date_range": "Date range",
        "filter_category": "Category",
        "filter_category_mode": "Text filter mode",
        "filter_contains": "Contains",
        "filter_starts": "Starts with",
        "filter_equals": "Equals",
        "filter_numeric": "Numeric filter",
        "filter_numeric_col": "Numeric column",
        "filter_numeric_range": "Value range",
        "filter_outliers": "Remove outliers (IQR)",
        "insights_title": "🧠 Automatic insights and descriptive statistics",
        "stats_title": "Descriptive statistics",
        "corr_title": "Correlation matrix between numeric variables",
        "top_cat_title": "Top 5 categories in {cat} by sum of {val}",
        "insights_list_title": "Insights in natural language",
        "outliers_title": "Outliers (IQR method)",
        "no_num_cols": "There are not enough numeric columns for descriptive statistics.",
        "no_outliers_info": "Outliers could not be calculated.",
        "viz_title": "📊 Visualizations",
        "select_num_col": "Select a numeric column for detailed analysis",
        "hist_title": "Distribution of {col}",
        "box_title": "Boxplot of {col} by {cat}",
        "bar_title": "Sum of {col} by {cat}",
        "line_title": "Evolution of {col} over time",
        "pdf_title_section": "📄 Generate PDF report (Professional Layout)",
        "pdf_button": "Generate PDF",
        "pdf_success": "PDF generated successfully!",
        "pdf_download": "Download PDF",
        "insight_num": "For {col}, the mean is {mean:,.2f}, median {median:,.2f}, standard deviation {std:,.2f}, minimum {min:,.2f} and maximum {max:,.2f}.",
        "insight_period": "The analyzed period goes from {start} to {end}.",
        "insight_topcat": "The top 5 categories in {cat}, considering the sum of {val}, were calculated to highlight concentrations.",
        "insight_corr": "Correlation between numeric variables was calculated to identify linear relationships.",
        "insight_outliers": "In {col}, {qtd} potential outliers were detected using the IQR method."
    }
}

# ---------------------------
# TEXTOS DO PDF (SEM ACENTOS)
# ---------------------------
T_PDF = {
    "pt": {
        "cover_title": "Relatorio Analitico",
        "cover_brand": "Platero Analytics — Data Intelligence",
        "summary": "Sumario",
        "sum_1": "1. Estatisticas descritivas",
        "sum_2": "2. Insights automaticos",
        "sum_3": "3. Outliers",
        "sum_4": "4. Primeiras linhas da planilha",
        "stats_section": "1. Estatisticas descritivas",
        "insights_section": "2. Insights automaticos",
        "outliers_section": "3. Outliers (metodo IQR)",
        "table_section": "4. Primeiras linhas da planilha",
        "cover_sub": "Gerado em {date}",
        "footer": "Platero Analytics — Pagina [page]",
        "no_num_cols": "Nao ha colunas numericas suficientes para estatisticas descritivas.",
        "no_outliers_info": "Nao foi possivel calcular outliers."
    },

    "en": {
        "cover_title": "Analytical Report",
        "cover_brand": "Platero Analytics — Data Intelligence",
        "summary": "Summary",
        "sum_1": "1. Descriptive statistics",
        "sum_2": "2. Automatic insights",
        "sum_3": "3. Outliers",
        "sum_4": "4. First rows of the spreadsheet",
        "stats_section": "1. Descriptive statistics",
        "insights_section": "2. Automatic insights",
        "outliers_section": "3. Outliers (IQR method)",
        "table_section": "4. First rows of the spreadsheet",
        "cover_sub": "Generated on {date}",
        "footer": "Platero Analytics — Page [page]",
        "no_num_cols": "There are not enough numeric columns for descriptive statistics.",
        "no_outliers_info": "Outliers could not be calculated."
    }
}
# ---------------------------
# FUNÇÃO DE LIMPEZA UNIVERSAL (VERSÃO CORRIGIDA)
# ---------------------------
def limpar_planilha(df):
    import numpy as np
    import pandas as pd

    # Remove linhas totalmente vazias
    df = df.dropna(how="all")

    # Remove colunas totalmente vazias
    df = df.dropna(axis=1, how="all")

    if df.empty:
        return df

    # Detecta melhor linha de cabeçalho (mais células preenchidas)
    melhor_linha = 0
    melhor_score = -1
    for i in range(min(10, len(df))):
        linha = df.iloc[i]
        score = linha.notna().sum()
        if score > melhor_score:
            melhor_score = score
            melhor_linha = i

    # Define cabeçalho real
    df.columns = df.iloc[melhor_linha].astype(str).fillna("").str.strip()
    df = df.iloc[melhor_linha + 1 :]

    # Garante que todos os nomes de colunas são strings válidas
    df.columns = [
        str(c).strip() if c is not None else f"coluna_{i}"
        for i, c in enumerate(df.columns)
    ]

    # Substitui nomes vazios ou inválidos
    df.columns = [
        col if col not in ["", "nan", "None"] else f"coluna_{i}"
        for i, col in enumerate(df.columns)
    ]

    # Remove colunas Unnamed
    df.columns = [
        col if not col.lower().startswith("unnamed") else f"coluna_{i}"
        for i, col in enumerate(df.columns)
    ]

    # Limpa nomes
    df.columns = (
        pd.Series(df.columns)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace("  ", " ", regex=False)
        .str.strip()
        .tolist()
    )

    # Converte números com vírgula
    for col in df.columns:
        try:
            if df[col].dtype == object:
                s = df[col].astype(str)
                s = s.str.replace(".", "", regex=False)
                s = s.str.replace(",", ".", regex=False)
                df[col] = pd.to_numeric(s, errors="ignore")
        except:
            pass

    # Converte datas
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="raise")
        except:
            pass

    df = df.dropna(how="all").reset_index(drop=True)
    return df


# ---------------------------
# FUNÇÃO AUXILIAR: FORMATAR DATA POR IDIOMA
# ---------------------------
def format_date(dt, lang):
    if pd.isna(dt):
        return ""
    if lang == "pt":
        return dt.strftime("%d/%m/%Y")
    else:
        return dt.strftime("%b %d, %Y")


# ---------------------------
# FUNÇÃO AUXILIAR: FILTROS AVANÇADOS
# ---------------------------
def apply_advanced_filters(df, datas, categoricas, numericas, lang):
    df_f = df.copy()
    st.subheader(T[lang]["filters_title"])

    # Filtro de datas
    if datas:
        col_data = datas[0]
        min_date = df_f[col_data].min()
        max_date = df_f[col_data].max()

        if pd.notna(min_date) and pd.notna(max_date):
            date_range = st.date_input(
                T[lang]["filter_date_range"],
                value=(min_date.date(), max_date.date())
            )
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start, end = date_range
                df_f = df_f[
                    (df_f[col_data] >= pd.to_datetime(start)) &
                    (df_f[col_data] <= pd.to_datetime(end))
                ]

    # Filtro de categoria
    if categoricas:
        col_cat = categoricas[0]
        st.markdown(f"**{T[lang]['filter_category']}:** {col_cat}")

        unique_vals = sorted(df_f[col_cat].dropna().astype(str).unique().tolist())
        selected_vals = st.multiselect(
            T[lang]["filter_category"],
            options=unique_vals,
            default=unique_vals
        )

        mode = st.selectbox(
            T[lang]["filter_category_mode"],
            [T[lang]["filter_contains"], T[lang]["filter_starts"], T[lang]["filter_equals"]]
        )

        if selected_vals:
            mask = False
            for val in selected_vals:
                if mode == T[lang]["filter_contains"]:
                    mask = mask | df_f[col_cat].astype(str).str.contains(val, case=False, na=False)
                elif mode == T[lang]["filter_starts"]:
                    mask = mask | df_f[col_cat].astype(str).str.startswith(val, na=False)
                else:
                    mask = mask | (df_f[col_cat].astype(str) == val)
            df_f = df_f[mask]

    # Filtro numérico
    if numericas:
        st.subheader(T[lang]["filter_numeric"])
        col_num = st.selectbox(T[lang]["filter_numeric_col"], numericas)

        serie = df_f[col_num].dropna()
        if not serie.empty:
            min_val = float(serie.min())
            max_val = float(serie.max())

            val_range = st.slider(
                T[lang]["filter_numeric_range"],
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val)
            )

            df_f = df_f[(df_f[col_num] >= val_range[0]) & (df_f[col_num] <= val_range[1])]

            # Remover outliers
            remove_out = st.checkbox(T[lang]["filter_outliers"])
            if remove_out:
                q1 = serie.quantile(0.25)
                q3 = serie.quantile(0.75)
                iqr = q3 - q1
                lim_inf = q1 - 1.5 * iqr
                lim_sup = q3 + 1.5 * iqr
                df_f = df_f[(df_f[col_num] >= lim_inf) & (df_f[col_num] <= lim_sup)]

    st.markdown("---")
    return df_f
# ---------------------------
# TOGGLE DE IDIOMA
# ---------------------------
col_lang1, _ = st.columns([1, 3])
with col_lang1:
    lang = st.radio(
        T["pt"]["language_label"],
        options=["pt", "en"],
        format_func=lambda x: T[x]["lang_pt"] if x == "pt" else T[x]["lang_en"]
    )

st.title(T[lang]["app_title"])
st.write(T[lang]["app_subtitle"])


# ---------------------------
# UPLOAD DO ARQUIVO
# ---------------------------
arquivo = st.file_uploader(T[lang]["upload_label"], type=["xlsx", "csv"], key="upload_unico")

if not arquivo:
    st.info(T[lang]["upload_hint"])
    st.stop()

nome = arquivo.name.lower()

# ---------------------------
# LEITURA SEGURA DO ARQUIVO
# ---------------------------
try:
    if nome.endswith(".xlsx"):
        df = pd.read_excel(arquivo)
    else:
        try:
            df = pd.read_csv(arquivo, sep=";")
        except:
            df = pd.read_csv(arquivo)
except:
    st.error(T[lang]["error_read"])
    st.stop()

if df.empty:
    st.error(T[lang]["error_empty"])
    st.stop()


# ---------------------------
# LIMPEZA AUTOMÁTICA UNIVERSAL
# ---------------------------
df = limpar_planilha(df)

if df.empty:
    st.error("Após limpeza, a planilha ficou vazia. Verifique o arquivo de origem.")
    st.stop()


# ---------------------------
# TRATAR COLUNAS DUPLICADAS
# ---------------------------
if df.columns.duplicated().any():
    st.warning(T[lang]["warn_dup_cols"])
    df.columns = [
        f"{col}_{i}" if df.columns.tolist().count(col) > 1 else col
        for i, col in enumerate(df.columns)
    ]


# ---------------------------
# DETECÇÃO DE TIPOS
# ---------------------------
datas = []
for col in df.columns:
    if pd.api.types.is_datetime64_any_dtype(df[col]):
        datas.append(col)

numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()


# ---------------------------
# PRÉVIA DOS DADOS
# ---------------------------
st.subheader(T[lang]["preview_title"])
st.dataframe(df.head())


# ---------------------------
# TIPOS DE COLUNAS
# ---------------------------
st.subheader(T[lang]["types_title"])
c1, c2, c3 = st.columns(3)

c1.write(f"**{T[lang]['num_cols']}:** {numericas if numericas else '-'}")
c2.write(f"**{T[lang]['date_cols']}:** {datas if datas else '-'}")
c3.write(f"**{T[lang]['cat_cols']}:** {categoricas if categoricas else '-'}")
# ---------------------------
# FILTROS AVANÇADOS
# ---------------------------
df_filtered = apply_advanced_filters(df, datas, categoricas, numericas, lang)


# ---------------------------
# INSIGHTS E ESTATÍSTICA
# ---------------------------
st.header(T[lang]["insights_title"])

insights = []
estatisticas_html = ""
outliers_info = ""


# ---------------------------
# ESTATÍSTICAS DESCRITIVAS
# ---------------------------
if numericas:
    desc = df_filtered[numericas].describe().T
    desc["coef_var"] = desc["std"] / desc["mean"]

    estatisticas_html = desc.to_html(float_format=lambda x: f"{x:,.2f}")

    st.subheader(T[lang]["stats_title"])
    st.dataframe(desc)

    # Insights numéricos
    for col in numericas:
        serie = df_filtered[col].dropna()
        if serie.empty:
            continue

        media = serie.mean()
        mediana = serie.median()
        maximo = serie.max()
        minimo = serie.min()
        desvio = serie.std()

        insights.append(
            T[lang]["insight_num"].format(
                col=col,
                mean=media,
                median=mediana,
                std=desvio,
                min=minimo,
                max=maximo
            )
        )

    # Correlação
    if len(numericas) > 1:
        corr = df_filtered[numericas].corr()
        st.subheader(T[lang]["corr_title"])
        st.dataframe(corr.style.background_gradient(cmap="Blues"))
        insights.append(T[lang]["insight_corr"])

else:
    estatisticas_html = ""


# ---------------------------
# INSIGHT DE PERÍODO (DATAS)
# ---------------------------
if datas:
    col_data = datas[0]
    serie_data = df_filtered[col_data].dropna()

    if not serie_data.empty:
        inicio = serie_data.min()
        fim = serie_data.max()

        insights.append(
            T[lang]["insight_period"].format(
                start=format_date(inicio, lang),
                end=format_date(fim, lang)
            )
        )


# ---------------------------
# TOP CATEGORIAS
# ---------------------------
if categoricas and numericas:
    col_cat = categoricas[0]
    col_val = numericas[0]

    agrupado = (
        df_filtered.groupby(col_cat)[col_val]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.subheader(T[lang]["top_cat_title"].format(cat=col_cat, val=col_val))
    st.dataframe(agrupado)

    insights.append(
        T[lang]["insight_topcat"].format(cat=col_cat, val=col_val)
    )


# ---------------------------
# OUTLIERS (IQR)
# ---------------------------
if numericas:
    outliers_info = "<ul>"

    for col in numericas:
        serie = df_filtered[col].dropna()
        if serie.empty:
            continue

        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        iqr = q3 - q1

        lim_inf = q1 - 1.5 * iqr
        lim_sup = q3 + 1.5 * iqr

        qtd_out = serie[(serie < lim_inf) | (serie > lim_sup)].shape[0]

        if lang == "pt":
            outliers_info += f"<li>{col}: {qtd_out} possiveis outliers detectados (IQR).</li>"
        else:
            outliers_info += f"<li>{col}: {qtd_out} potential outliers detected (IQR).</li>"

        if qtd_out > 0:
            insights.append(
                T[lang]["insight_outliers"].format(col=col, qtd=qtd_out)
            )

    outliers_info += "</ul>"


# ---------------------------
# EXIBIR INSIGHTS
# ---------------------------
st.subheader(T[lang]["insights_list_title"])

for item in insights:
    st.write("- " + item)
    # ---------------------------
# GRÁFICOS (APENAS NO APP)
# ---------------------------
st.header(T[lang]["viz_title"])

if numericas:
    col_num = st.selectbox(T[lang]["select_num_col"], numericas)

    # Histograma
    fig_hist = px.histogram(
        df_filtered,
        x=col_num,
        nbins=30,
        title=T[lang]["hist_title"].format(col=col_num)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Boxplot por categoria
    if categoricas:
        col_cat_box = categoricas[0]
        fig_box = px.box(
            df_filtered,
            x=col_cat_box,
            y=col_num,
            title=T[lang]["box_title"].format(col=col_num, cat=col_cat_box)
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # Barras por categoria
    if categoricas:
        col_cat_bar = categoricas[0]
        df_bar = (
            df_filtered.groupby(col_cat_bar)[col_num]
            .sum()
            .reset_index()
        )
        fig_bar = px.bar(
            df_bar,
            x=col_cat_bar,
            y=col_num,
            title=T[lang]["bar_title"].format(col=col_num, cat=col_cat_bar)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# Série temporal
if datas and numericas:
    col_data = datas[0]
    col_valor = numericas[0]

    df_temp = (
        df_filtered[[col_data, col_valor]]
        .dropna()
        .sort_values(by=col_data)
    )

    if not df_temp.empty:
        fig_line = px.line(
            df_temp,
            x=col_data,
            y=col_valor,
            title=T[lang]["line_title"].format(col=col_valor)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        # ---------------------------
# PDF (SEM GRÁFICOS — TEXTO + TABELA)
# ---------------------------
st.header(T[lang]["pdf_title_section"])

if st.button(T[lang]["pdf_button"]):

    now = datetime.now()
    data_atual = format_date(now, lang)

    pdf_txt = T_PDF[lang]

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

    # HTML do PDF
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #000; }}
            h1, h2 {{ color: #003366; }}
            .header {{
                display: flex;
                align-items: center;
                gap: 20px;
                border-bottom: 2px solid #003366;
                padding-bottom: 10px;
                margin-bottom: 30px;
            }}
            .footer {{
                position: fixed;
                bottom: 10px;
                width: 100%;
                text-align: center;
                font-size: 12px;
                color: #003366;
            }}
            .capa {{
                text-align: center;
                margin-top: 150px;
            }}
            .capa h1 {{ font-size: 40px; }}
            .capa h3 {{ color: #555; }}
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
        <h1>{pdf_txt["cover_title"]}</h1>
        <h3>{pdf_txt["cover_sub"].format(date=data_atual)}</h3>
        <h3>{pdf_txt["cover_brand"]}</h3>
    </div>

    <!-- CABEÇALHO -->
    <div class="header">
        <div>{logo_svg}</div>
        <h2>{pdf_txt["cover_brand"]}</h2>
    </div>

    <!-- SUMÁRIO -->
    <h2>{pdf_txt["summary"]}</h2>
    <p>{pdf_txt["sum_1"]}</p>
    <p>{pdf_txt["sum_2"]}</p>
    <p>{pdf_txt["sum_3"]}</p>
    <p>{pdf_txt["sum_4"]}</p>

    <!-- ESTATÍSTICAS -->
    <h2>{pdf_txt["stats_section"]}</h2>
    {estatisticas_html if estatisticas_html else f"<p>{pdf_txt['no_num_cols']}</p>"}

    <!-- INSIGHTS -->
    <h2>{pdf_txt["insights_section"]}</h2>
    {''.join(f'<p>• {i}</p>' for i in insights)}

    <!-- OUTLIERS -->
    <h2>{pdf_txt["outliers_section"]}</h2>
    {outliers_info if outliers_info else f"<p>{pdf_txt['no_outliers_info']}</p>"}

    <!-- PRIMEIRAS LINHAS -->
    <h2>{pdf_txt["table_section"]}</h2>
    {df_filtered.head().to_html()}

    <div class="footer">{pdf_txt["footer"]}</div>

    </body>
    </html>
    """

    # Criar arquivo temporário HTML
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_html:
        tmp_html.write(html.encode("utf-8"))
        tmp_html_path = tmp_html.name

    # Caminho do PDF
    pdf_path = tmp_html_path.replace(".html", ".pdf")

    # Opções do PDF
    options = {
        "encoding": "UTF-8",
        "footer-center": "[page]",
        "footer-font-size": "10"
    }

    # Gerar PDF
    pdfkit.from_file(tmp_html_path, pdf_path, options=options)

    # Ler PDF
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # Botão de download
    st.success(T[lang]["pdf_success"])
    st.download_button(
        T[lang]["pdf_download"],
        data=pdf_bytes,
        file_name="relatorio_profissional.pdf"
    )