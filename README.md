# Lens Inventory Market

Application d'analyse d'images et génération automatique d'annonces utilisant l'IA.

## Fonctionnalités

- Détection d'objets en temps réel
- Analyse d'images via Google Lens (SerpAPI)
- Génération automatique d'annonces optimisées
- Support multi-plateformes sociales
- Interface API REST

## Configuration

1. Créer un fichier `.env` avec vos clés API:
```
SERPAPI_API_KEY=votre_clé_serpapi
```

2. Installer les dépendances:
```bash
pip install -r requirements.txt
```

3. Lancer l'application:
```bash
python main.py
```

## Structure du Projet

- `main.py`: Point d'entrée de l'application
- `crews/`: Définitions des crews spécialisés
- `agents/`: Agents AI spécialisés
- `services/`: Services d'analyse et de traitement
- `utils/`: Utilitaires communs
