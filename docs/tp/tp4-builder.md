# TP 4 : Builder, la pizza sur mesure

**Partir de** `etape-3` · **Solution** `etape-4`

```
git switch -c tp4-binome-a origin/etape-3
```

## Objectif

`make_custom_pizza()` prend six paramètres, dont trois listes de garnitures. On l'appelle en se trompant d'ordre, et elle laisse passer des pizzas que les règles interdisent. Remplacez-la par un Builder : la pizza se construit étape par étape, et **toutes** les règles sont vérifiées au moment de `build()`.

## 1. Lire les règles

Comparez `make_custom_pizza()` (dans `src/pronto/menu.py`) avec la section « La pizza sur mesure » de `docs/regles-metier.md`. Deux règles ne sont pas vérifiées : lesquelles ?

## 2. Coder le Builder

Créez `src/pronto/pizza_builder.py` :

```python
pizza = PizzaBuilder().size("L").dough("fine").left("jambon").right("chevre", "miel").build()
```

- Les étapes `size()`, `dough()`, `base()`, `topping()`, `left()` et `right()` renvoient le builder lui-même (annotez-les `-> Self`, de `typing`). `topping()`, `left()` et `right()` acceptent plusieurs garnitures (`*toppings`). Une moitié sans garniture compte comme absente.
- `build()` vérifie toutes les règles et lève `InvalidPizza` (une sous-classe de `ValueError`) au premier problème.
- `WebReader` utilise le builder, et `make_custom_pizza()` disparaît. Une `InvalidPizza` remonte telle quelle jusqu'à l'appelant.

### Tests à faire passer

Dans `tests/test_pizza_builder.py` (il remplace `tests/test_menu.py`) :
- `test_a_custom_pizza_costs_its_size_plus_its_toppings`
- `test_a_size_is_required`
- `test_an_unknown_base_is_refused`
- `test_a_custom_pizza_has_at_most_six_toppings`
- `test_half_and_half_is_only_for_large_pizzas`
- `test_each_half_has_at_least_one_topping`
- `test_a_half_and_half_pizza_counts_the_toppings_of_both_halves` : une L avec `left("jambon", "olives").right("chevre")` coûte 17,50 €

Et dans `tests/test_intake.py` : `test_a_web_order_can_contain_a_custom_pizza`.

## 3. Un builder pour les tests

Relisez `tests/test_pricing.py` : chaque test construit sa commande à la main avec la fonction `order_of()` et ses paramètres. Écrivez `tests/builders.py` :

```python
order = an_order().with_pizza("reine", 2).with_promo_code("ETUDIANT").for_a_student().build()
```

Prévoyez aussi `with_pizza(name, quantity=1)` et `placed_at(when: datetime)` pour fixer l'heure de la commande : le test du happy hour en a besoin, et le TP 6 aussi. Par défaut, la commande est passée le 3 novembre 2026 à midi.

Importez-le avec `from tests.builders import an_order`, puis réécrivez `tests/test_pricing.py` avec. Les noms des tests ne changent pas.

## 4. Kata Prototype (10 min)

`katas/prototype/reorder.py` permet de « recommander » une commande passée. Lancez `pytest katas/prototype` : trois tests échouent. Le premier rappelle qu'une commande recommandée repart à l'état `validée`.
- Pourquoi modifier la nouvelle commande modifie-t-elle l'ancienne ?
- Pourquoi ajouter une garniture à une pizza commandée modifie-t-il **le menu** ?

Corrigez `reorder()`, puis `menu_pizza()` : le menu devient un **registre de prototypes**, qui donne une copie de son modèle à chaque appel. Outils : `copy.copy`, `copy.deepcopy`, `dataclasses.replace`.

## Discuter

- En Python, les arguments nommés et une `dataclass` remplacent souvent le Builder. Qu'est-ce qui le justifie ici ?
- Un Builder et une « interface fluide », est-ce la même chose ?

## Pour aller plus loin

Dans SQLAlchemy, `select(Order).where(...).order_by(...)` est un Builder de requête. Chaque étape renvoie **une copie** de la requête : l'original ne change pas. C'est le Prototype au service du Builder. Vérifiez-le dans un shell (après `pip install sqlalchemy`) : `q1 = select(...)`, `q2 = q1.where(...)`, puis `q1 is q2` ?
