-- 02_window_rank.sql - TOP produit par ville avec WINDOW FUNCTION
WITH ca_par_produit_ville AS (
  SELECT 
    c.ville, 
    v.produit, 
    SUM(v.quantite * v.prix_unitaire) as total_ca
  FROM clients c 
  LEFT JOIN ventes v ON c.client_id = v.client_id
  GROUP BY c.ville, v.produit
),
classement AS (
  SELECT 
    ville, 
    produit, 
    total_ca,
    RANK() OVER (PARTITION BY ville ORDER BY total_ca DESC) as rang
  FROM ca_par_produit_ville
)
SELECT * FROM classement WHERE rang = 1;