from pronto.countries import kit_for
from pronto.order import Order
from pronto.pricing import compute_total


def euros(cents: int) -> str:
    return f"{cents // 100},{cents % 100:02d} €"


def render_invoice(order: Order) -> str:
    total = compute_total(order)
    formatter = kit_for(order.customer.country).create_invoice_formatter()
    header = formatter.header()
    vat_rate = formatter.vat_rate()

    vat = total.amount * vat_rate // (100 + vat_rate)
    lines = [header, f"Commande n° {order.number}"]
    lines += [f"{line.quantity} x {line.pizza.name} : {euros(line.total)}" for line in order.lines]
    if total.discount:
        lines.append(f"Remise {order.promo_code} : -{euros(total.discount)}")
    lines.append(f"Livraison : {euros(total.delivery_fee)}")
    lines.append(f"Total TTC : {euros(total.amount)} (dont TVA {vat_rate} % : {euros(vat)})")
    return "\n".join(lines)
