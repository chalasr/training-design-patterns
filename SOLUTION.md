# Étape 4 : solution du TP 4 (Builder) et du kata Prototype

## Le Builder

- `PizzaBuilder` construit la pizza sur mesure étape par étape : `size()`, `dough()`, `base()`, `topping()`, `left()`, `right()`, puis `build()`.
- **Toutes** les règles sont vérifiées dans `build()`, au moment où la pizza est complète. C'est là seulement qu'on peut vérifier les règles qui portent sur l'ensemble : le total des garnitures, le moitié-moitié en taille L avec une garniture de chaque côté.
- Deux règles manquaient dans `make_custom_pizza()` : la base n'était pas vérifiée, et une seule moitié garnie passait.
- `build()` donne des **copies** des listes de garnitures. Le builder peut resservir sans que la pizza construite change.
- `tests/builders.py` : `an_order().with_pizza("reine", 2).for_a_student().build()`. Les tests ne disent plus que ce qui compte pour eux, le reste prend une valeur par défaut.

## Fallait-il un Builder ?

- Avec des arguments nommés (`custom_pizza(size="L", left=[...])`), l'appel serait aussi lisible.
- Le Builder se justifie par la construction **en plusieurs étapes**, avec une validation d'ensemble à la fin. Ici, `WebReader` ajoute les garnitures au fil du JSON.
- Une interface fluide (des méthodes qui renvoient `self`) n'est qu'une forme d'écriture. Le pattern, c'est de séparer la construction de l'objet construit.

## Le kata Prototype

- `copy.copy()` copie la commande, mais **pas ses listes** : les deux commandes partagent les mêmes `OrderLine`.
- `reorder()` utilise désormais `dataclasses.replace()`, avec `copy.deepcopy()` pour les lignes. Il remet aussi l'état à `validée`.
- `menu_pizza()` rendait **l'objet du menu lui-même** : une garniture ajoutée sur une pizza commandée s'ajoutait au menu. Le menu est maintenant un registre de prototypes : `menu_pizza()` rend une copie profonde du modèle.
- Avec des objets immuables (`frozen=True`, des tuples), la question ne se pose plus : `replace()` suffit.

## Ce qui reste

`OrderService` appelle encore en dur le SMS, la cuisine et la fidélité. Le TP 5 s'en occupe.
