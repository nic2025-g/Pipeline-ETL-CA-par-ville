-- 01_ca_par_ville.sql - VERT du 24/09 19h
-- Objectif: CA par ville en gardant Paris avec LEFT JOIN

CREATE TABLE clients (client_id INT, ville TEXT);
INSERT INTO clients VALUES (1,'Marseille'), (2,'Paris'), (3,'USA');

CREATE TABLE ventes (client_id INT, quantite INT, prix_unitaire INT);
INSERT INTO ventes VALUES (1,10,200), (1,1,50), (3,2,50);

WITH ca_par_ville AS (
 SELECT c.ville, COALESCE(SUM(v.quantite * v.prix_unitaire),0) AS total_ca
 FROM clients c LEFT JOIN ventes v ON c.client_id = v.client_id
 GROUP BY c.ville
)
SELECT * FROM ca_par_ville;
-- Résultat attendu: Marseille 2050 / Paris 0 / USA 100