# WordPress Log Generator

Un script Python pour générer des logs WordPress réalistes incluant du trafic normal et des tentatives d'attaque depuis une IP spécifique.

## Description

Ce script génère des fichiers de logs WordPress simulés qui incluent :
- Du trafic web normal avec des user-agents légitimes
- Des activités de reconnaissance (scanning)
- Des tentatives d'attaque ciblées depuis une IP spécifique
- Une distribution réaliste des requêtes sur une période donnée

## Installation

Aucune dépendance externe n'est requise. Le script utilise uniquement la bibliothèque standard Python 3.

## Utilisation

```bash
python3 genfakewplog.py YYYY-MM-DD YYYY-MM-DD IP_ATTAQUANT
```

### Exemples

```bash
python3 genfakewplog.py 2024-03-15 2024-03-17 45.33.22.211
```

### Paramètres

- `YYYY-MM-DD` : Date de début de la période
- `YYYY-MM-DD` : Date de fin de la période
- `IP_ATTAQUANT` : Adresse IP qui sera utilisée pour les attaques simulées

## Sortie

Le script génère :
- Un fichier de log au format `wordpress_YYYYMMDD_YYYYMMDD.log`
- Un résumé dans la console avec :
  - Le nom du fichier généré
  - La période couverte
  - Le nombre total de lignes
  - Le nombre d'attaques simulées

## Format des logs

Les logs générés suivent le format standard des logs Apache :
```
IP - - [DATE:HEURE +0000] "METHODE CHEMIN HTTP/1.1" STATUS TAILLE "-" "USER_AGENT" "DATA"
```