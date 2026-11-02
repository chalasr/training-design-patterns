# TP 2 : Factory Method, les canaux de commande

**Partir de** `etape-1` · **Solution** `etape-2`

```
git switch -c tp2-binome-a origin/etape-1
```

## Objectif

`OrderIntake.receive()` lit trois formats de commande dans un seul `if/elif`, puis applique un traitement commun : vérifier la commande, l'enregistrer. Pronto ouvre un quatrième canal, la **borne de commande** en boutique. Ajoutez-le sans toucher au traitement commun.

## 1. Repérer ce qui varie

Dans `src/pronto/intake.py`, séparez au surligneur :
- ce qui change d'un canal à l'autre ;
- ce qui est identique pour tous les canaux.

## 2. Coder

- **Le produit.**
  - `OrderReader` (un `Protocol`) : `read(payload) -> ReceivedOrder`.
  - `ReceivedOrder` est une `dataclass` qui regroupe `customer`, `lines` et `promo_code`.
- **Le créateur.**
  - `OrderIntake` devient une classe abstraite. Sa méthode `receive(payload, now)` contient le traitement commun.
  - Elle obtient son lecteur par la **méthode de fabrication** abstraite `create_reader()`.
- **Les créateurs concrets.** `WebIntake`, `PhoneIntake` et `PartnerIntake` déclarent leur `channel` et redéfinissent `create_reader()`. Rien d'autre.
- **Les produits concrets.** `WebReader`, `PhoneReader` et `PartnerReader` : déplacez-y tel quel le code de chaque branche du `if/elif`.
- **Le point d'entrée.** Dans `app.py`, le champ `intake` d'`App` devient `intakes: dict[str, OrderIntake]` (un intake par `channel`). `App` gagne une méthode `receive_order(channel, payload, now)`, qui choisit l'intake du canal et lève `InvalidOrder` pour un canal inconnu. La fixture `receive_order` renvoie `app.receive_order`.
- **Le nouveau canal.** Ajoutez `KioskReader` et `KioskIntake`, la borne, sur le canal `"kiosk"`. Son format :
  ```python
  {"phone": "+33612345678", "pizzas": ["reine", "reine", "margherita"]}
  ```
  Le client s'appelle « Client borne », il est en France, et la borne n'accepte pas de code promo.

### Tests à faire passer

Dans `tests/test_intake.py` :
- `test_each_channel_reads_its_own_format` : une commande par canal (web, phone, partner), passée par `receive_order` ; vérifiez `order.channel` et le client lu
- `test_a_kiosk_order_groups_identical_pizzas`
- `test_an_unknown_channel_is_refused`

`tests/test_order_journey.py` reste vert sans modification.

## 3. Comparer avec la forme pythonique (sur papier)

En Python, une classe est déjà une fabrique : on l'appelle. Esquissez, sans la coder, une variante où `OrderIntake` n'est plus abstraite et reçoit la **classe** du lecteur : `OrderIntake(service, reader_class=WebReader)`.

Laquelle préférez-vous ? Et quand la sous-classe se justifie-t-elle ?

## Pour aller plus loin

Flask utilise les deux formes :
- des méthodes de fabrication à redéfinir dans une sous-classe de `Flask` : `create_jinja_environment()`, `make_config()` ;
- des attributs de classe : `response_class`, `request_class`.

Pourquoi les deux ?
