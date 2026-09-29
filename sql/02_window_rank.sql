-- 02_window_rank.sql - TOP produit par ville avec WINDOW FUNCTION
-- Fix: on recrée les tables AVEC la colonne produit

DROP TABLE IF EXISTS ventes;
DROP TABLE IF EXISTS clients;

CREATE TABLE clients (client_id INT, ville TEXT);
INSERT INTO clients VALUES 
(1,'Marseille'), 
(2,'Paris'), 
(3,'USA');

CREATE TABLE ventes (client_id INT, produit TEXT, quantite INT, prix_unitaire INT);
INSERT INTO ventes VALUES 
(1,'Chaise',10,200), 
(1,'Table',1,50), 
(3,'Chaise',2,50),
(1,'Chaise',5,200),
(3,'Table',10,50);

-- Maintenant le test VERT pour ce soir
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
-- remplace ta dernière ligne par ça :
SELECT 
  ville, 
  COALESCE(produit, 'AUCUNE VENTE') as produit,
  COALESCE(total_ca, 0) as total_ca,
  rang
FROM classement 
WHERE rang = 1;