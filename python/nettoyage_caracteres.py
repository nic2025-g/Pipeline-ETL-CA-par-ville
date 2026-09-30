import pandas as pd

def nettoyer_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie un DataFrame :
    - colonnes en minuscule + trim
    - valeurs texte en minuscule + trim
    - garde les chiffres intacts
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip().str.lower()
            # remet les vrais 'nan' en NA si on a stringifié des NaN
            df[col] = df[col].replace({'nan': pd.NA, 'none': pd.NA, 'null': pd.NA})

    return df

# Ce bloc ne s'exécute QUE si tu lances le fichier tout seul
# Il ne s'exécute PAS quand tu fais "from nettoyage_caracteres import nettoyer_df"
if __name__ == "__main__":
    df_test = pd.DataFrame({
        " Produit ": [" Laptop ", "LAPTOP ", " souris"],
        " Prix ": [100, 100, 20]
    })
    print("AVANT :")
    print(df_test)
    print("\nAPRES nettoyer_df :")
    print(nettoyer_df(df_test))