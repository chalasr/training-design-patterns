# TP 5 : Observer, le suivi de commande

**Partir de** `etape-4` · **Solution** `etape-5`

```
git switch -c tp5-binome-a origin/etape-4
```

## Objectif

À chaque changement d'état d'une commande, `OrderService` appelle lui-même la passerelle SMS, l'écran de la cuisine et le programme de fidélité. Le service connaît ainsi tous ceux que la commande intéresse.

Pronto veut maintenant **prévenir les coursiers** quand une commande sort du four. Faites en sorte que ce nouvel intéressé s'ajoute sans modifier `OrderService`.

## 1. Repérer les intéressés

Dans `src/pronto/service.py`, listez tout ce qui se passe **après** le changement d'état. Qui a besoin de savoir quoi ?

## 2. Coder

- **L'événement.** `OrderStatusChanged` est une `dataclass` figée qui porte la commande. Créez-la dans `src/pronto/events.py`.
- **Le sujet.** `Publisher`, dans le même fichier :
  - `subscribe(subscriber)` enregistre un abonné, c'est-à-dire n'importe quel callable qui reçoit un `OrderStatusChanged` ;
  - `notify(event)` prévient les abonnés, dans l'ordre d'abonnement.
- **Le service.** `OrderService` reçoit un `Publisher` et le notifie dans `place()` et `advance()`. Il ne connaît plus ni le SMS, ni la cuisine, ni la fidélité.
- **Les abonnés.** Dans `src/pronto/subscribers.py` : `SmsNotifier`, `KitchenDisplay` et `LoyaltyRewarder`.
- **Les dépendances.**
  - Les instances globales `KITCHEN_SCREEN` et `LOYALTY` disparaissent : `create_app()` crée l'écran et le programme de fidélité, puis abonne chacun.
  - `App` expose `publisher`, `kitchen_screen`, `loyalty` et `courier_board`.
  - `OUTBOX` reste global : il simule le monde extérieur, les SMS réellement envoyés.
- **Le nouvel abonné.** Créez dans `notifications.py` un `CourierBoard`, sur le modèle de `KitchenScreen` : une liste `lines` et une méthode `post(text)`. `CourierDispatch` y écrit `#12 à livrer : Alice` quand la commande passe `en livraison`.
- **La validation.** `place()` notifie aussi : l'événement porte alors une commande `validée`. Le SMS de validation a son propre texte (voir `tests/test_order_journey.py`).
- **La robustesse.** Un abonné qui lève une exception ne doit empêcher ni les autres abonnés, ni le changement d'état. `Publisher` journalise l'erreur avec `logging` et continue.

### Tests à faire passer

Dans `tests/test_order_tracking.py` :
- `test_every_subscriber_is_notified_in_subscription_order`
- `test_a_failing_subscriber_does_not_block_the_others`
- `test_couriers_are_called_when_an_order_leaves_the_oven`

`tests/test_order_journey.py` reste vert sans modification. Dans `tests/conftest.py`, la fixture automatique ne vide plus que `OUTBOX`, et les fixtures `kitchen_screen` et `loyalty` renvoient `app.kitchen_screen` et `app.loyalty`. Le test des coursiers lit `app.courier_board`.

## Discuter

- Un abonné est un simple callable. Faut-il une classe `Subscriber` abstraite ?
- Le `Publisher` garde une référence vers chaque abonné. Quand est-ce un problème ? (Voir `weakref`.)
- Un abonné lent ralentit `advance()`. Comment l'éviter ?
- Les abonnés dépendent-ils de l'ordre dans lequel on les prévient ? Devraient-ils ?

## Pour aller plus loin

Vous utilisez déjà ce pattern :
- les signaux de Flask (`request_started`, `template_rendered`...) reposent sur `blinker` : `signal.connect(subscriber)`, puis `signal.send(sender)` ;
- SQLAlchemy a ses événements : `event.listen(Session, "before_flush", subscriber)`.

Quelle différence voyez-vous avec votre `Publisher` ?
