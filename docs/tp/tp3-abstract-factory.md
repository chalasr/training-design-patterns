# TP 3 : Abstract Factory, Pronto au Luxembourg

**Partir de** `etape-2` · **Solution** `etape-3`

```
git switch -c tp3-binome-a origin/etape-2
```

## Objectif

Le pays du client décide de trois choses : la validation du téléphone, la passerelle SMS et la facture. Aujourd'hui, `if country == "FR"` est écrit à trois endroits. Pronto ouvre au Luxembourg.

La règle à garantir : **on ne mélange jamais deux pays**. Un client belge a une validation belge, un SMS belge et une facture belge.

## 1. Repérer la famille

Cherchez `country` dans `src/pronto`. Pour chaque endroit, notez ce qui dépend du pays.

## 2. Coder

Créez `src/pronto/countries.py`. Les interfaces vous sont données :

```python
class PhoneValidator(Protocol):
    def is_valid(self, phone: str) -> bool: ...


class SmsGateway(Protocol):
    def send(self, phone: str, message: str) -> None: ...


class InvoiceFormatter(Protocol):
    def header(self) -> str: ...

    def vat_rate(self) -> int: ...  # un pourcentage entier : 10 pour 10 %


class CountryKit(Protocol):
    def create_phone_validator(self) -> PhoneValidator: ...

    def create_sms_gateway(self) -> SmsGateway: ...

    def create_invoice_formatter(self) -> InvoiceFormatter: ...
```

- **Les produits concrets.** Une passerelle par fournisseur (`SmsFranceGateway`, `BelSmsGateway`), un validateur et une facture par pays. Vous pouvez paramétrer un même produit (un validateur par expression régulière, par exemple).
- **Les fabriques concrètes.** `FranceKit` et `BelgiumKit`.
- **Le choix du pays.** `kit_for(country)` rend la fabrique du pays et lève `UnservedCountry` pour un pays non desservi. `OrderIntake.receive()` convertit cette erreur en `InvalidOrder`. Les trois `if country` disparaissent, ainsi que `send_sms()` dans `notifications.py`.
- **Le nouveau pays.** Ajoutez `LuxembourgKit`, code pays `"LU"`, sans modifier le code qui utilise les fabriques :
  - téléphone : `+352` suivi de 6 à 9 chiffres ;
  - passerelle SMS : `LuxSms` ;
  - facture : en-tête « Pronto Luxembourg SARL - 2 place de la Burrata, 1111 Luxembourg », TVA 3 %.

Les passerelles SMS écrivent toujours dans `OUTBOX`, avec le nom du fournisseur : ce sont des simulations.

### Tests à faire passer

Dans `tests/test_countries.py` :
- `test_a_kit_creates_products_of_a_single_country` : pour chaque fabrique, le validateur accepte un numéro du pays et refuse celui d'un autre, la passerelle envoie par le bon fournisseur, la facture porte la bonne société
- `test_a_luxembourg_order_is_validated_texted_and_invoiced_in_luxembourg`
- `test_an_unserved_country_is_refused` : `kit_for("DE")` lève `UnservedCountry`

`tests/test_order_journey.py` reste vert sans modification.

## 3. Discuter

- Les fabriques concrètes sont-elles des Singletons ? Faut-il le garantir ?
- Ici, une bonne partie de la famille est de la **donnée** (un préfixe, un nom, un taux). Une `dataclass` figée par pays suffirait-elle ? Qu'est-ce qui justifie la fabrique ?
- SQLAlchemy fait la même chose avec ses dialectes : chaque `Dialect` (PostgreSQL, SQLite...) fournit sa famille de compilateurs. Pourquoi ne mélange-t-on jamais le compilateur SQL de PostgreSQL avec le compilateur de types de SQLite ?
