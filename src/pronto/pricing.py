from dataclasses import dataclass

from pronto.order import Order

DELIVERY_FEE = 250
FREE_DELIVERY_FROM = 2500


class PromotionRefused(Exception):
    pass


@dataclass(frozen=True)
class Total:
    subtotal: int
    discount: int
    delivery_fee: int

    @property
    def amount(self) -> int:
        return self.subtotal - self.discount + self.delivery_fee


def compute_total(order: Order) -> Total:
    subtotal = order.subtotal
    discount = 0
    if order.promo_code is None:
        discount = 0
    elif order.promo_code == "ETUDIANT":
        if not order.customer.is_student:
            raise PromotionRefused("Code réservé aux étudiants")
        discount = subtotal * 20 // 100
    elif order.promo_code == "HAPPYHOUR":
        if order.placed_at.hour == 18:
            discount = subtotal * 10 // 100
    elif order.promo_code == "3POUR2":
        prices = sorted(line.pizza.price for line in order.lines for _ in range(line.quantity))
        discount = sum(prices[: len(prices) // 3])
    else:
        raise PromotionRefused(f"Code inconnu : {order.promo_code}")

    delivery_fee = 0 if subtotal - discount >= FREE_DELIVERY_FROM else DELIVERY_FEE
    return Total(subtotal, discount, delivery_fee)
