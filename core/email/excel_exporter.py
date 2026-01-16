import pandas as pd
from io import BytesIO

def exportar_excel(df):
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados Filtrados")

        workbook = writer.book
        worksheet = writer.sheets["Dados Filtrados"]

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#0A1A2F",
            "font_color": "white",
            "border": 1
        })

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 18)

    return buffer.getvalue()