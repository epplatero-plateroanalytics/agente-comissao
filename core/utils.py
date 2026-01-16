def detectar_tipos(df):
    datas = []
    numericas = []
    categoricas = []

    for col in df.columns:
        if str(df[col].dtype).startswith("datetime"):
            datas.append(col)
        elif str(df[col].dtype).startswith(("float", "int")):
            numericas.append(col)
        else:
            categoricas.append(col)

    return datas, numericas, categoricas