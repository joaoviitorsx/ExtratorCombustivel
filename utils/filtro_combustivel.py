import pandas as pd

def filtrar_diesel(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra os itens que são Diesel com base no NCM e na descrição"""
    return df[
        df["Descrição"].str.lower().str.contains("diesel", na=False) &
        (df["NCM"] == "27101921")
    ].copy()

def filtrar_gasolina(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra os itens que são Gasolina com base no NCM e na descrição"""
    return df[
        df["Descrição"].str.lower().str.contains("gasolina", na=False) &
        (df["NCM"] == "27101259")
    ].copy()
