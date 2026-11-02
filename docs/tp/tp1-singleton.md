# TP 1 : Singleton, l'écrire puis s'en passer

**Partir de** `etape-0` · **Solution** `etape-1`

```
git switch -c tp1-binome-a origin/etape-0
```

Remplacez `binome-a` par le nom de votre binôme.

## Objectif

Savoir écrire un Singleton en Python, puis reconnaître le problème qu'il pose quand il sert d'accès global : `Database.instance()` est appelé partout dans Pronto.

## 1. Kata : trois singletons

Dans `katas/singleton/singletons.py`, faites passer `pytest katas/singleton` :

| Variante | À écrire |
|---|---|
| `ConfigWithNew` | un Singleton par `__new__` |
| `ConfigWithMetaclass` | `SingletonMeta.__call__`, une métaclasse réutilisable |
| `get_config()` | une fonction qui renvoie toujours la même `AppConfig`, sans toucher à la classe |

Complétez aussi la fixture `forget_instances` : chaque test doit repartir des réglages par défaut.

Le test `test_a_setting_changed_once_is_seen_everywhere` vous réserve une surprise avec `__new__` : cherchez qui remet les réglages par défaut.

Comparez ensuite les trois variantes, à l'oral :
- que se passe-t-il au deuxième appel de `ConfigWithNew()` si vous oubliez `__init__` ?
- laquelle supporte l'héritage ?
- laquelle est sûre si deux threads l'appellent en même temps ?

Le dernier test, déjà vert, rappelle qu'**un module Python est déjà un singleton**.

## 2. Diagnostic

- Lisez `src/pronto/database.py`, puis `tests/conftest.py`.
- Supprimez la ligne `Database.reset_instance()` de la fixture, puis lancez `pytest`. Quels tests échouent, et pourquoi ?
- Lancez maintenant un seul de ces tests, par exemple `pytest tests/test_order_journey.py -k numbered`. Que constatez-vous ?
- Remettez la ligne en place.

Question : qui, dans le code, sait que `OrderRepository` a besoin d'une base de données ?

## 3. Refactoring

Faites disparaître `Database.instance()` et `Database.reset_instance()` :
- `OrderRepository` reçoit sa `Database` dans son constructeur ;
- `OrderService` reçoit son repository, et `OrderIntake` son service ;
- un module `src/pronto/app.py` expose `create_app(database_path=None) -> App` :
  - la fonction crée la `Database` de l'application, puis assemble les objets dans une `dataclass` `App` (`database`, `orders`, `service`, `intake`) ;
  - c'est la **racine de composition**, comme la fabrique `create_app()` d'une application Flask ;
  - une application a une seule base, et chaque appel crée une application neuve.

Dans `tests/conftest.py`, une fixture `app` appelle `create_app(":memory:")`, et les autres fixtures (`receive_order`, `service`, `orders`) en tirent leurs objets. Chaque test a donc sa propre base. `tests/test_order_journey.py` ne change pas.

Les TP suivants partent de cette structure.

## Pour aller plus loin

`notifications.py` contient d'autres singletons : `OUTBOX`, `KITCHEN_SCREEN`, `LOYALTY`. Sont-ils un problème ? On les retrouvera au TP 5.
