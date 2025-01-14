# Projet Django : Pokédex et Mini-jeu de Combat

## Description du projet

Ce projet de cours a pour but d'explorer le framework Django à travers le développement d'une application web qui servira de Pokédex et inclura un mini-jeu de combat. L'objectif est de créer une interface utilisateur où les visiteurs peuvent consulter les informations sur différents Pokémon et participer à des combats simulés.

## Objectifs

- **Pokédex :** Créer une base de données de Pokémon avec des détails tels que le nom, type, statistiques et une brève description.
- **Mini-jeu de Combat :** Développer un jeu interactif où les utilisateurs peuvent choisir un Pokémon pour combattre contre un adversaire contrôlé par l'ordinateur.

## Technologies utilisées

- **HTML** : Utilisé pour structurer le contenu de nos pages web.
- **Python (Django)** : Django servira de framework back-end pour gérer les interactions entre l'utilisateur, le serveur, et la base de données.
- **JavaScript : pour la manipulation du dom.

## Équipe

- **Emilia Beguin** - B3 DEV I, option Data Science
- **Romain Merceron** - B3 EV IA, option Data Science
- **David Chardon** - B3 DEV IA, option Data Science
- **Thibaut Mosteau** - B3 DEV IA, FullStack

## Installtation avec docker Docker

Créer l'image Docker "croquidex" :
```bash
docker build -t croquidex .
```

Vérifier que `croquiDex` fait bien partie des images Docker disponibles :
```bash
docker images
```

Exécuter un conteneur à partir de l'image `croquidex` et le lier au port 8000 :
```bash
docker run --name CroquiDex -p 8000:8000 croquidex
```

Supprimer le conteneur "CroquiDex" si besoin de le recréer par exemple:
```bash
docker container rm CroquiDex
```


## Installation sans docker 

```bash
pip install -r requirements.txt
```

```bash
mkdir -p /Users/thibaut/Desktop/CroquiDex/static
```

```bash
pip install openai
```

```bash
python3 manage.py runserver
```