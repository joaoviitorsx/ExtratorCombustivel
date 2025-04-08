import pandas as pd
import re

def identificar_pneu(nome_produto):
    """
    Detecta se um nome de produto indica que se trata de um pneu ou carcaça de pneu.
    """
    if not isinstance(nome_produto, str):
        return False

    nome = nome_produto.lower()
    
    # Palavras-chave que indicam pneu/carcaça
    palavras_chave = [
        "pneu", "carcaça", "carcaca", "295/80", "275/80", "rodagem", "borracha", "banda", "205/55", "g359", "g560"
    ]

    for palavra in palavras_chave:
        if palavra in nome:
            return True

    # Regex para padrões de medidas de pneu
    if re.search(r"\d{3}/\d{2,3}r\d{2}", nome):
        return True

    return False

def filtrar_pneu(df):
    """
    Filtra os produtos que parecem ser pneus com base no nome/descritivo.
    """
    nome_coluna = None
    colunas_possiveis = ["Nome Produto", "xProd", "Descrição", "Produto"]

    for col in colunas_possiveis:
        if col in df.columns:
            nome_coluna = col
            break

    if not nome_coluna:
        print("Nenhuma coluna de nome de produto foi encontrada para identificar pneus.")
        return pd.DataFrame()

    df_filtrado = df[df[nome_coluna].apply(identificar_pneu)].copy()
    return df_filtrado
