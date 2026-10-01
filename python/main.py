import pandas as pd
import sqlite3
from pathlib import Path
from nettoyage_caracteres import nettoyer_df

# --- Chemins pro ---
ROOT = Path(__file__).parent.parent
DATA = ROOT / "data" / "ventes.csv"
SQL_01 = ROOT / "sql" / "01_ca_par_ville.sql"
SQL_02 = ROOT / "sql" / "02_window_rank.sql"

print(f"--- ETL Pipeline : {ROOT.name} ---")

# 1. Données clients (en dur pour l'instant)
clients = [(101, "Nicolas", "Marseille"), (102, "John", "USA"), (103, "Ines", "Paris")]
df_client = pd.DataFrame(clients, columns=["client_id", "nom", "ville"])

# 2. Ventes : on crée data/ventes.csv si il n'existe pas
if not DATA.exists():
    pd.DataFrame([
        [1, "Laptop", 2, 1000, 101],
        [2, "Souris", 5, 20, 102],
        [3, "Clavier", 1, 50, 101]
    ], columns=["id", "produit", "quantite", "prix_unitaire", "client_id"]).to_csv(DATA, index=False)

df_ventes = pd.read_csv(DATA)

# 3. Nettoyage (ta fonction de ce matin)
print("\nAVANT nettoyage :")
print(df_ventes.head())
df_ventes = nettoyer_df(df_ventes)  # met produit en minuscule
print("\nAPRES nettoyage :")
print(df_ventes.head())

df_ventes["ca"] = df_ventes["quantite"]*df_ventes["prix_unitaire"]

# 4. Python: LEFT JOIN + fillna = COALESCE
df_final = pd.merge(df_client, df_ventes, on="client_id", how="left")
df_final["ca"] = df_final["ca"].fillna(0)
resultat_python = df_final.groupby("ville")["ca"].sum().reset_index()
print("\n--- Python: CA par ville ---")
print(resultat_python)

# 5. SQL: on exécute ton fichier 01
conn = sqlite3.connect(":memory:")
df_client.to_sql("clients", conn, index=False, if_exists="replace")
df_ventes.to_sql("ventes", conn, index=False, if_exists="replace")

# On lit le SQL depuis sql/01_ca_par_ville.sql
sql_01 = SQL_01.read_text(encoding='utf-8')
# On ne garde que la requête WITH (pas les CREATE pour ce test mémoire)
sql_query = """
WITH ventes_nettoye AS (
    SELECT c.ville, COALESCE(v.quantite * v.prix_unitaire, 0) as ca_final
    FROM clients c LEFT JOIN ventes v ON c.client_id = v.client_id
)
SELECT ville, SUM(ca_final) as ca_total FROM ventes_nettoye GROUP BY ville
"""

print("\n--- SQL: CTE + COALESCE ---")
print(pd.read_sql_query(sql_query, conn))

# 6. SQL Window (ton 02)
print("\n--- SQL: 02_window_rank.sql ---")
# print(pd.read_sql_query("SELECT ville, produit, SUM(quantite * prix_unitaire) as total_ca FROM clients c LEFT JOIN ventes v ON c.client_id = v.client_id GROUP BY ville, produit", conn))"""

# remplace la dernière ligne print par :
sql_rank = """
WITH ca_par_produit AS (
  SELECT c.ville, v.produit, SUM(v.quantite * v.prix_unitaire) as total_ca
  FROM clients c LEFT JOIN ventes v ON c.client_id = v.client_id
  GROUP BY c.ville, v.produit
)
SELECT ville, 
       COALESCE(produit, 'AUCUNE VENTE') as produit,
       COALESCE(total_ca, 0) as total_ca,
       RANK() OVER (PARTITION BY ville ORDER BY total_ca DESC) as rang
FROM ca_par_produit
"""

# --- SQL 02 depuis le fichier ---
with open(ROOT / "sql" / "02_window_rank.sql", "r", encoding="utf-8") as f:
    sql_02 = f.read()
# On enlève les commentaires et on garde seulement le dernier SELECT si besoin, 
# mais ici ton fichier est déjà propre
print("\n--- SQL 02: TOP produit par ville ---")
print(pd.read_sql_query(sql_02, conn))

# print(pd.read_sql_query(sql_rank, conn))