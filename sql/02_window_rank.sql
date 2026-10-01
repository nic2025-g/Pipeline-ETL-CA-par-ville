-- 02_window_rank.sql - TOP 1 produit par ville
-- Pas de DROP TABLE, on utilise les vraies tables créées par main.py

WITH ca_par_produit_ville AS (
  SELECT
    c.ville,
    v.produit,
    SUM(v.quantite * v.prix_unitaire) AS total_ca
  FROM clients c
  LEFT JOIN ventes v ON c.client_id = v.client_id
  GROUP BY c.ville, v.produit
),
classement AS (
  SELECT
    ville,
    produit,
    total_ca,
    RANK() OVER (PARTITION BY ville ORDER BY total_ca DESC) AS rang
  FROM ca_par_produit_ville
)
SELECT
  ville,
  COALESCE(produit, 'AUCUNE VENTE') AS produit,
  COALESCE(total_ca, 0) AS total_ca,
  rang
FROM classement
WHERE rang = 1
ORDER BY ville;