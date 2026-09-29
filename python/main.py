import pandas as pd
# Creation d'un fichier en mode écriture

pd.DataFrame([
    [1, "laptop", 2, 1000, 101],
    [2, "souris", 5, 20,102],
    [3, "clavier", 1, 50, 101]
], columns=["id", "produit", "quantite", "prix_unitaire", "client_id"]).to_csv("ventes.csv", index=False)
    
import sqlite3

# Donnees

clients = [(101, "Nicolas", "Marseille"), (102, "John", "USA"), (103, "Ines", "Paris")]

df_client = pd.DataFrame(clients, columns=["client_id", "nom", "ville"])

df_ventes = pd.read_csv("ventes.csv")
df_ventes["ca"] = df_ventes["quantite"]*df_ventes["prix_unitaire"]

# Python: LEFT JOIN + fillna = COALESCE

df_final = pd.merge(df_client, df_ventes, on= "client_id", how="left")

df_final["ca"] = df_final["ca"].fillna(0)

resultat_python = df_final.groupby("ville")["ca"].sum().reset_index()

print("  --- Python: CA par ville ---")
print(resultat_python)

# SQL: CTE + COALESCE

conn = sqlite3.connect(":memory:")

df_client.to_sql("clients", conn, index=False, if_exists = "replace")
df_ventes.to_sql("ventes", conn, index=False, if_exists = "replace")

sql ="""

WITH ventes_nettoye AS (
    SELECT
        c.ville,
        COALESCE (v.quantite * v.                                 prix_unitaire, 0) as ca_final
    FROM clients c 
    LEFT JOIN ventes v on c.client_id = v.             client_id
)

SELECT ville , SUM(ca_final) as ca_total
FROM ventes_nettoye
GROUP BY ville
"""
print("\n --- SQL: CTE + COALESCE --- ")
print(pd.read_sql_query(sql, conn))