# Étape 0 : le code de départ

Pas de solution sur cette branche : c'est le point de départ du TP 1.

Ce code marche, et ses tests sont verts. Il résiste pourtant au changement :
- `Database.instance()` est appelé partout ;
- trois `if/elif` différents décident selon le canal, le pays ou le code promo ;
- `OrderService.advance()` appelle en dur le SMS, la cuisine et la fidélité.
