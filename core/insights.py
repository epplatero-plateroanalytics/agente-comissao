import pandas as pd  # <--- Certifique-se de importar o pandas no topo

def gerar_kpis(df, colunas_numericas):
    kpis = {}
    
    for col in colunas_numericas:
        if col in df.columns:
            # --- CORREÇÃO AQUI ---
            # Tenta converter para número. Se der erro (texto), vira NaN (vazio)
            # Isso resolve problemas de números vindo como texto
            serie_numerica = pd.to_numeric(df[col], errors='coerce')
            
            kpis[col] = {
                "soma": serie_numerica.sum(),
                "media": serie_numerica.mean(),
                "max": serie_numerica.max(),
                "min": serie_numerica.min()
            }
            # ---------------------
            
    return kpis