# TP 7 : Command, annuler et rétablir dans le panier

**Partir de** `etape-6` · **Solution** `etape-7`

```
git switch -c tp7-binome-a origin/etape-6
```

## Objectif

Sur le site, le client veut **annuler** sa dernière action dans le panier (`Ctrl+Z`), puis la **rétablir**. Aujourd'hui, `Cart` modifie son contenu directement et ne garde aucune trace de ce qui s'est passé.

## 1. Lister les actions

Pour chaque méthode de `src/pronto/cart.py`, répondez : que faut-il **mémoriser** pour pouvoir l'annuler ?

## 2. Coder

Dans `src/pronto/cart_commands.py` :
- **La commande.** `CartCommand` (un `Protocol`) : `execute()` et `undo()`.
- **Les commandes concrètes.** Chacune reçoit le panier à sa création.
  - `AddPizza(cart, "reine", 2)` : son annulation retire les 2 pizzas ajoutées, pas toute la ligne.
  - `RemovePizza(cart, "reine")` retient la quantité retirée.
  - `ApplyCoupon(cart, "ETUDIANT")` retient le code précédent.
- **L'invocateur.** `CartHistory` : `run(command)`, `undo()`, `redo()`.
  - Annuler ou rétablir quand il n'y a rien à faire ne fait rien.
  - Une nouvelle action efface les actions qu'on pouvait rétablir.

Il vous faudra peut-être une méthode de plus sur `Cart`, et `apply_coupon()` devra accepter `None` (pour revenir à « pas de code »).

### Tests à faire passer

Dans `tests/test_cart_history.py` :
- `test_adding_a_pizza_can_be_undone`
- `test_undoing_an_addition_keeps_the_pizzas_added_before`
- `test_a_removed_pizza_comes_back_with_its_quantity_on_undo`
- `test_undoing_a_coupon_restores_the_previous_one`
- `test_an_undone_action_can_be_redone`
- `test_a_new_action_clears_the_redo_history`

## Discuter

- Une commande sans annulation, c'est une fonction : `functools.partial(cart.add, "reine", 2)`. Qu'apporte la classe ?
- Faut-il mémoriser l'action (la commande) ou l'état du panier avant l'action ? Quels sont les coûts de chaque option ?

## Bonus : les tickets de cuisine

Une commande est un objet : on peut la **mettre en file**, la journaliser, la rejouer.

Dans `src/pronto/kitchen.py`, écrivez `PrepareOrder(number)`, sérialisable en JSON (`to_json()` et `from_json()`). Son `execute(service)` met la commande au four (`service.advance(number)`). Mettez-la dans une `queue.Queue`, puis faites-la exécuter par un « four » qui la dépile. C'est ce que font Celery et RQ avec vos tâches.

## Pour aller plus loin

Une migration Alembic est une commande avec annulation : `upgrade()` et `downgrade()`. `alembic downgrade -1`, c'est votre `undo()`.
