import pandas as pd

def nettoyer_df(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    for col in df.columns:
        # on vérifie si c'est du texte (object)
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip().str.lower()
    return df

# ✅ Bonne création de DataFrame pour tester ton bug "Laptop vs LAPTOP"
df_test = pd.DataFrame({
    " Produit ": [" Laptop ", "LAPTOP ", " souris"],
    " Prix ": [100, 100, 20]
})

print("AVANT : ")
print(df_test)

print("\nAPRÈS nettoyer_df :")
print(nettoyer_df(df_test))

###############################################################
# Objectif : le pipeline qui ne crash jamais                  #
#                                                             #
# Énoncé : Crée ventes.csv puis lis-le avec gestion d'erreur. #
###############################################################

with open("ventes.csv","w", encoding="utf-8") as f: 
    f.write("id,produit,prix\n")
    f.write("1,clavier,50\n")
    f.write("2,souris,20\n")
 
try:
    df_ventes = pd.read_csv("ventes.csv")
    print("La moyenne des prix de ventes est: ", df_ventes["prix"].mean())
    #print(df_ventes["prix"].mean())
except FileNotFoundError:
    print("Fichier manquant")

