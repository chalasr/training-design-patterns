# Étape 3 : solution du TP 3 (Abstract Factory)

- `countries.py` regroupe la famille de chaque pays :
  - les trois produits : `PhoneValidator`, `SmsGateway`, `InvoiceFormatter` ;
  - la fabrique abstraite `CountryKit` ;
  - les fabriques concrètes `FranceKit`, `BelgiumKit` et `LuxembourgKit`.
- Les trois `if country` ont disparu. Chaque lieu demande sa fabrique à `kit_for(country)`, puis le produit dont il a besoin. Un client belge ne peut plus recevoir un SMS français avec une facture belge : tout vient de la même fabrique.
- Le Luxembourg s'ajoute avec deux classes (`LuxembourgKit`, `LuxSmsGateway`) et une entrée dans `KITS`. `intake.py`, `service.py` et `invoice.py` n'ont pas changé.
- Les fabriques sont sans état : une instance par pays, créée une fois dans `KITS`. C'est une unicité **par construction**, pas un Singleton imposé par la classe.

## Fallait-il une fabrique ?

- Le validateur et la facture sont surtout de la **donnée** : un motif, un nom de société, un taux. Une `dataclass` figée par pays suffirait pour eux.
- La fabrique se justifie par les passerelles SMS : en production, chacune parle à une API différente. C'est du **comportement**.
- Elle se justifie aussi par la règle de cohérence : la famille vient d'un seul endroit.
- SQLAlchemy procède de même : chaque `Dialect` fournit ses propres compilateurs (`statement_compiler`, `ddl_compiler`, `type_compiler_cls`), qui ne se mélangent jamais avec ceux d'un autre dialecte.

## Ce qui reste

`OrderService` appelle encore en dur la passerelle SMS, l'écran de la cuisine et la fidélité. Le TP 5 s'en occupe.
