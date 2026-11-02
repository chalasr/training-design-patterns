# Étape 1 : solution du TP 1 (Singleton)

## Le kata

- `ConfigWithNew` : `__new__` crée l'instance une seule fois. Il faut aussi neutraliser `__init__` : Python l'appelle **à chaque** `ConfigWithNew()`, et il remettrait les réglages par défaut.
- `SingletonMeta` : la métaclasse intercepte l'appel de la classe (`__call__`). Elle se réutilise sur n'importe quelle classe, et chaque sous-classe a sa propre instance.
- `get_config()` : `functools.cache` garde le résultat du premier appel. La classe reste une classe ordinaire, qu'on peut instancier librement dans les tests.
- Les deux premières variantes prennent un verrou : sans lui, deux threads peuvent créer chacun leur instance.
- La fixture `forget_instances` doit connaître l'intérieur de chaque variante pour la remettre à zéro. C'est le prix d'un état global.

## Pronto

- `Database.instance()` et `Database.reset_instance()` ont disparu : chaque objet **reçoit** ce dont il a besoin dans son constructeur.
- `app.py`, avec `create_app()`, est la racine de composition. Elle crée **la seule** `Database` de l'application et assemble les objets, comme la fabrique d'application de Flask.
- Il y a toujours une seule base par application : le besoin d'unicité est tenu par l'assemblage, pas par la classe.
- Les tests créent une application neuve par test : plus aucun test ne dépend de l'ordre d'exécution.
- `tests/test_order_journey.py` n'a pas changé.

## Ce qui reste

`OUTBOX`, `KITCHEN_SCREEN` et `LOYALTY` sont encore des instances globales de module. Le TP 5 s'en occupe.
