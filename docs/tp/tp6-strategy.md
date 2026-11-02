# TP 6 : Strategy, les promotions

**Partir de** `etape-5` · **Solution** `etape-6`

```
git switch -c tp6-binome-a origin/etape-5
```

## Objectif

`compute_total()` choisit la remise dans un `if/elif` sur le code promo. Chaque nouvelle promotion oblige à modifier ce calcul, que tous les canaux utilisent.

Le marketing lance le code `MARDI` : 2 € de remise par pizza, le mardi uniquement. Ajoutez-le **sans toucher à `compute_total()`**.

## 1. Repérer l'algorithme qui varie

Dans `src/pronto/pricing.py`, qu'est-ce qui change d'une promotion à l'autre ? Qu'est-ce qui reste identique (la livraison, le total) ?

## 2. Coder

- **La stratégie.** `Promotion` (un `Protocol`) : `discount(order) -> int`, en centimes. Une promotion refusée lève `PromotionRefused`.
- **Les stratégies concrètes.** `StudentDiscount`, `HappyHour`, `ThreeForTwo`.
- **Le choix.** `PROMOTIONS` associe chaque code à sa stratégie. `compute_total()` choisit la stratégie par le code promo de la commande, et ne connaît aucune promotion en particulier.
- **La nouvelle promotion.** `TuesdayDeal`, enregistrée sous le code `MARDI` : 2 € par pizza le mardi, rien les autres jours. La remise ne dépasse jamais le sous-total.

Attention : la date par défaut du builder de test (le 3 novembre 2026) est un mardi. Fixez la date avec `placed_at()` pour tester les autres jours.

### Tests à faire passer

Dans `tests/test_pricing.py`, les tests existants restent verts. Ajoutez :
- `test_on_tuesdays_each_pizza_is_2_euros_off`
- `test_the_tuesday_code_gives_nothing_on_other_days`

## 3. Comparer avec des fonctions (dans un fichier de brouillon)

Une stratégie sans état et à une seule méthode est une fonction. Réécrivez deux promotions en fonctions, sans les garder dans le code : le corrigé garde les classes.

```python
def three_for_two(order: Order) -> int: ...


PROMOTIONS = {"3POUR2": three_for_two, "ETUDIANT": percent_off_for_students(20)}
```

`mypy` refusera ce dictionnaire tant qu'il est typé `dict[str, Promotion]` : pourquoi ? Quel type lui donner ?

Qu'est-ce qui se lit le mieux ? Quand la classe redevient-elle utile (paramètres, nom affiché sur la facture, plusieurs méthodes) ?

## Pour aller plus loin

Vous passez déjà des stratégies tous les jours :
- `sorted(orders, key=lambda order: order.placed_at)` ;
- les stratégies de chargement des relations SQLAlchemy : `relationship(lazy="selectin")`, ou `options(joinedload(...))` ;
- les stratégies d'attente de `tenacity` : `@retry(wait=wait_exponential())`.
