# Étape 6 : solution du TP 6 (Strategy)

- `Promotion` est la stratégie : `discount(order)` rend la remise en centimes, ou lève `PromotionRefused`.
- Les stratégies concrètes sont `StudentDiscount`, `HappyHour`, `ThreeForTwo` et `TuesdayDeal`. Elles portent leurs paramètres (`percent`, `hour`, `per_pizza`) : le taux de la remise étudiante change sans toucher au code.
- `PROMOTIONS` associe chaque code à sa stratégie. `compute_total()` ne connaît plus aucune promotion : il choisit la stratégie par le code, puis calcule la livraison et le total.
- `MARDI` s'ajoute avec une classe et une entrée dans `PROMOTIONS`. `compute_total()` n'a pas changé.

## La forme pythonique

Une stratégie sans état et à une seule méthode est une fonction :

```python
def three_for_two(order: Order) -> int:
    prices = sorted(line.pizza.price for line in order.lines for _ in range(line.quantity))
    return sum(prices[: len(prices) // 3])


PROMOTIONS: dict[str, Callable[[Order], int]] = {"3POUR2": three_for_two, ...}
```

Pour une stratégie paramétrée, `functools.partial(percent_off, 20)` ou une fonction qui renvoie une fonction suffisent.

La classe redevient utile quand la stratégie a :
- des paramètres qu'on veut afficher ou comparer (une `dataclass` figée les montre dans le `repr`) ;
- plusieurs méthodes, par exemple un libellé pour la facture en plus du calcul ;
- un état.

## Dans votre quotidien

- `sorted(orders, key=...)` : la clé de tri est une stratégie.
- SQLAlchemy : `relationship(lazy="selectin")` choisit la stratégie de chargement des relations.
- `tenacity` : `@retry(wait=wait_exponential())` choisit la stratégie d'attente.

## Ce qui reste

Le panier ne sait pas annuler la dernière action. Le TP 7 s'en occupe.
