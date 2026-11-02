# Étape 7 : solution du TP 7 (Command)

- `CartCommand` est la commande : `execute()` et `undo()`.
- Chaque commande concrète reçoit le panier (le récepteur) à sa création, et **mémorise ce qu'il faut pour s'annuler** :
  - `AddPizza` connaît la quantité ajoutée : son annulation la retire avec `Cart.withdraw()`, sans toucher aux pizzas ajoutées avant ;
  - `RemovePizza` retient la quantité qu'elle a retirée ;
  - `ApplyCoupon` retient le code précédent.
- `CartHistory` est l'invocateur. Il exécute les commandes et garde deux piles, les actions faites et les actions annulées. Une nouvelle action vide la seconde : on ne rétablit pas une action qui ne suit plus l'état du panier.
- `Cart` a gagné `withdraw()`, l'opération inverse de `add()`. Ses autres méthodes n'ont pas changé, et `Cart` ne sait rien de l'historique.
- Une commande qui échoue (retirer une pizza absente) lève son exception avant d'entrer dans l'historique.

## Mémoriser l'action ou l'état ?

- L'autre option est de mémoriser **l'état** du panier avant chaque action, avec `copy.deepcopy(cart)`. C'est le pattern Memento.
- Elle est plus simple à écrire et ne peut pas se tromper sur l'inverse. En revanche, elle coûte une copie complète par action et ne dit pas **ce qui** a été fait.
- La commande, elle, se journalise, se sérialise et se rejoue.

## La forme pythonique

Une commande sans annulation est un callable : `functools.partial(cart.add, "reine", 2)`, puis `command()`. C'est l'annulation, la mise en file ou la journalisation qui justifient la classe.

## Dans votre quotidien

- Une migration Alembic est une commande avec annulation : `upgrade()` et `downgrade()`. `alembic downgrade -1` est un `undo()`.
- Une tâche Celery ou RQ est une commande mise en file, exécutée par un autre processus.

## Bonus non corrigé

Les tickets de cuisine sérialisés (`PrepareOrder`) ne sont pas dans cette solution.
