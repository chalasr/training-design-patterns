# Étape 5 : solution du TP 5 (Observer)

- `events.py` :
  - `OrderStatusChanged` est l'événement, qui porte la commande ;
  - `Publisher` est le sujet : `subscribe()` enregistre un abonné, `notify()` prévient les abonnés dans l'ordre d'abonnement.
- `OrderService` ne connaît plus que le `Publisher`. Le SMS, la cuisine et la fidélité sont des abonnés, dans `subscribers.py` : `SmsNotifier`, `KitchenDisplay`, `LoyaltyRewarder`.
- `CourierDispatch` s'ajoute avec une classe et une ligne dans `create_app()`. `OrderService` n'a pas changé : c'est l'objectif du TP.
- Un abonné est **n'importe quel callable** qui reçoit l'événement. Les abonnés de Pronto sont des classes à `__call__`, parce qu'ils ont une dépendance (l'écran, le programme de fidélité) ; une `lambda` suffit dans les tests.
- `KITCHEN_SCREEN` et `LOYALTY` ne sont plus globaux : `create_app()` les crée et les donne aux abonnés. `OUTBOX` reste global, parce qu'il simule le monde extérieur.
- Un abonné qui lève une exception est journalisé (`logging.exception`) puis ignoré. Le changement d'état est déjà enregistré, et les autres abonnés sont prévenus.

## Les limites à connaître

- Les abonnés s'exécutent **dans** `advance()`, l'un après l'autre : un abonné lent ralentit tout. En production, on publie dans une file (Celery, RQ) et les abonnés travaillent à part.
- Le `Publisher` garde une référence forte vers chaque abonné. `blinker` utilise des références faibles par défaut, pour qu'un abonné oublié ne reste pas en vie.
- Avalé sans bruit, une erreur est perdue : la journaliser est le minimum.

## Dans Flask et SQLAlchemy

- `blinker`, sous les signaux de Flask : `request_started.connect(subscriber)`, puis `signal.send(app)`.
- SQLAlchemy : `event.listen(Session, "before_flush", subscriber)`.

## Ce qui reste

`compute_total()` choisit la promotion dans un `if/elif`. Le TP 6 s'en occupe.
