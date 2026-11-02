# Pronto : règles métier

Pronto est une pizzeria qui livre à domicile, en France et en Belgique (et au Luxembourg à partir du TP 3). Les commandes arrivent par trois canaux, sont préparées en cuisine puis livrées.

Les montants sont en centimes (`int`). Les noms des sociétés, les adresses et les taux de TVA de la facture sont **des données fictives** : le sujet de la formation n'est pas la fiscalité.

## Le menu

| Pizza | Prix |
|---|---|
| `margherita` | 9,00 € |
| `reine` | 11,00 € |
| `quatre-fromages` | 12,50 € (base crème) |
| `calzone` | 12,00 € |

## La pizza sur mesure (site web uniquement)

- Taille : S (8,00 €), M (10,00 €) ou L (13,00 €).
- Pâte : `classique`, `fine` ou `complete`. Base : `tomate` ou `creme`.
- Chaque garniture coûte 1,50 €. **Au plus 6 garnitures**, toutes moitiés confondues.
- **Moitié-moitié** : en taille L uniquement, avec au moins une garniture sur chaque moitié.

## Les canaux de commande

| Canal | Format reçu |
|---|---|
| `web` | Le panier du site, en JSON : client, pizzas du menu ou sur mesure, code promo |
| `phone` | La saisie de l'employé : une ligne `nom;téléphone;pays`, puis une ligne par pizza (`2 reine`) |
| `partner` | La plateforme partenaire, en JSON : références `PZ-REINE`, `PZ-MARG`, `PZ-4FROM`, `PZ-CALZ` |

Une commande contient au moins une pizza. Le téléphone du client doit être valide pour son pays : `+33` suivi de 9 chiffres (France), `+32` suivi de 8 ou 9 chiffres (Belgique).

## Le prix

- Livraison : 2,50 €, **offerte dès 25,00 €** (après remise).
- Codes promo, un seul par commande :

| Code | Règle |
|---|---|
| `ETUDIANT` | -20 % sur les pizzas, réservé aux clients étudiants |
| `HAPPYHOUR` | -10 % pour une commande passée entre 18h00 et 18h59 |
| `3POUR2` | Par lot de trois pizzas, la moins chère est offerte |
| `MARDI` (à partir du TP 6) | -2 € par pizza le mardi, sans dépasser le prix des pizzas |

## Le suivi de commande

`validée` → `au four` → `en livraison` → `livrée`.

À chaque étape :
- le client reçoit un SMS, par la passerelle de son pays (`SmsFrance` ou `BelSms`) ;
- la cuisine voit la commande à sa validation et à son passage au four ;
- à la livraison, le client gagne 1 point de fidélité par euro payé (arrondi à l'euro inférieur).

## La facture, par pays

| Pays | En-tête | TVA |
|---|---|---|
| France | Pronto France SAS - 12 rue de la Pâte, 75011 Paris | 10 % |
| Belgique | Pronto Belgique SRL - 4 rue de la Mozzarella, 1000 Bruxelles | 6 % |
| Luxembourg (TP 3) | Pronto Luxembourg SARL - 2 place de la Burrata, 1111 Luxembourg | 3 % |
