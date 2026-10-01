# Pipeline ETL - CA par ville

Projet Data Engineering : calcul du chiffre d'affaires par ville sans perdre les clients sans achats.

## Business Question
> Comment garder Paris à 0 au lieu de le perdre, et quel est le TOP produit par ville ?

## Architecture

Pipeline-ETL-CA-par-ville/
├── data/ventes.csv
├── sql/
│ ├── 01_ca_par_ville.sql (LEFT JOIN + COALESCE)
│ └── 02_window_rank.sql (RANK() OVER PARTITION BY)
├── python/
│ ├── main.py (pipeline principal)
│ └── nettoyage_caracteres.py (lib de nettoyage)
└── requirements.txt

## Stack & Compétences
- **ETL Python:** pandas, merge, groupby, pathlib
- **SQL:** LEFT JOIN, COALESCE, CTE (WITH), RANK() OVER (PARTITION BY)
- **Data Quality:** Gestion des NULL, jointure sans perte, normalisation produit

## Résultat
Marseille | 2050 | laptop (2000)
Paris | 0 | AUCUNE VENTE <- conservé grâce au LEFT JOIN
USA | 100 | souris (100


## Lancer le projet
```powershell
pip install -r requirements.txt
python .\python\main.py

Stack: Python, pandas, SQLite.