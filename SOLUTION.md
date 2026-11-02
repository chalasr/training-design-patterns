# Étape 2 : solution du TP 2 (Factory Method)

- **Ce qui varie** : la lecture du format reçu. **Ce qui ne varie pas** : vérifier la commande, puis l'enregistrer.
- `OrderIntake.receive()` porte le traitement commun. Il obtient son lecteur par la méthode de fabrication `create_reader()`, que chaque canal redéfinit.
- Le canal `kiosk` s'ajoute avec deux classes (`KioskReader`, `KioskIntake`) et une ligne dans `create_app()`. `OrderIntake.receive()` n'a pas changé : le code est ouvert à l'extension, fermé à la modification.
- `App.receive_order()` joue le rôle des routes de l'application : un canal, un intake.

## La forme pythonique

En Python, une classe est un callable : elle peut servir de fabrique sans sous-classe.

```python
class OrderIntake:
    def __init__(self, service: OrderService, reader_class: type[OrderReader]) -> None:
        self.service = service
        self.reader_class = reader_class

    def receive(self, payload: Any, now: datetime) -> Order:
        received = self.reader_class().read(payload)
        ...

OrderIntake(service, reader_class=KioskReader)
```

Elle est plus courte, et c'est souvent le bon choix. La sous-classe se justifie quand le canal redéfinit **plusieurs** choses à la fois (son lecteur, son nom, une étape de validation...), ou quand le framework impose l'héritage.

Flask fait les deux : `Flask.create_jinja_environment()` est une méthode de fabrication à redéfinir, `Flask.response_class` une classe passée en attribut.

## Ce qui reste

`OrderIntake.receive()` teste encore le pays du client. Le TP 3 s'en occupe.
