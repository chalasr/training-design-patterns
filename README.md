# Pronto : projet de travaux pratiques, formation Design Patterns

Pronto est une pizzeria qui livre à domicile, en France et en Belgique. Ce dépôt est le code des travaux pratiques des jours 1 et 2.

Il part d'un code qui marche mais qui résiste au changement (branche `etape-0`). TP après TP, on y introduit un pattern **là où le code en a besoin**.

- Les règles métier : [docs/regles-metier.md](docs/regles-metier.md)
- Les énoncés des TP : [docs/tp/](docs/tp/)

## Prérequis

- **Python 3.12 ou plus récent** et **Git**. Vérification : `python3 --version` et `git --version`.
- Un éditeur : PyCharm ou VS Code avec l'extension Python.

## Installation (une seule fois)

```
git clone https://github.com/chalasr/training-design-patterns.git pronto
cd pronto
python3 -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
```

Avec `uv` : `uv venv && uv pip install -r requirements-dev.txt`, puis `uv run pytest`.

Aucune dépendance en dehors des outils de développement : le code n'utilise que la bibliothèque standard.

## Vérifier son travail

```
pytest                     # les tests du projet
pytest -v                  # les tests, lus comme des phrases métier
pytest katas/singleton     # les tests d'un kata
ruff check . && ruff format --check .
mypy
```

## Déroulé des TP

Chaque étape corrigée a sa branche. **Chaque TP démarre de la branche de l'étape précédente**, dans une branche à vous (le préfixe `origin/` est nécessaire : après le clone, seule la branche par défaut, `etape-0`, existe en local) :

```
git switch -c tp1-binome-a origin/etape-0
```

| TP | Pattern | Partir de | Solution |
|---|---|---|---|
| [TP 1](docs/tp/tp1-singleton.md) | Singleton | `etape-0` | `etape-1` |
| [TP 2](docs/tp/tp2-factory-method.md) | Factory Method | `etape-1` | `etape-2` |
| [TP 3](docs/tp/tp3-abstract-factory.md) | Abstract Factory | `etape-2` | `etape-3` |
| [TP 4](docs/tp/tp4-builder.md) | Builder (et kata Prototype) | `etape-3` | `etape-4` |
| [TP 5](docs/tp/tp5-observer.md) | Observer | `etape-4` | `etape-5` |
| [TP 6](docs/tp/tp6-strategy.md) | Strategy | `etape-5` | `etape-6` |
| [TP 7](docs/tp/tp7-command.md) | Command | `etape-6` | `etape-7` |

En retard ou bloqué ? Repartez de la solution : `git switch -c tp3-binome-a origin/etape-2`. Chaque branche contient un `SOLUTION.md` qui explique ses choix. Pour voir exactement ce qu'une étape a changé : `git diff origin/etape-1 origin/etape-2`.

Le test `tests/test_order_journey.py` passe **à toutes les étapes, sans modification** : c'est le filet de sécurité de chaque refactoring.

## L'IA pendant les TP

Écrivez le code vous-mêmes : c'est en écrivant un pattern qu'on l'apprend. L'assistant sert de **relecteur** une fois votre version écrite (voir [AGENTS.md](AGENTS.md)).
