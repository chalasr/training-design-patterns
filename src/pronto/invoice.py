from pronto.order import Order
from pronto.pricing import compute_total


def euros(cents: int) -> str:
    return f"{cents // 100},{cents % 100:02d} €"


def render_invoice(order: Order) -> str:
    total = compute_total(order)
    if order.customer.country == "FR":
        header = "Pronto France SAS - 12 rue de la Pâte, 75011 Paris"
        vat_rate = 10
    elif order.customer.country == "BE":
        header = "Pronto Belgique SRL - 4 rue de la Mozzarella, 1000 Bruxelles"
        vat_rate = 6
    else:
        raise ValueError(f"Pays non desservi : {order.customer.country}")

    vat = total.amount * vat_rate // (100 + vat_rate)
    lines = [header, f"Commande n° {order.number}"]
    lines += [f"{line.quantity} x {line.pizza.name} : {euros(line.total)}" for line in order.lines]
    if total.discount:
        lines.append(f"Remise {order.promo_code} : -{euros(total.discount)}")
    lines.append(f"Livraison : {euros(total.delivery_fee)}")
    lines.append(f"Total TTC : {euros(total.amount)} (dont TVA {vat_rate} % : {euros(vat)})")
    return "\n".join(lines)
