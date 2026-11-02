from dataclasses import dataclass
from typing import Protocol

from pronto.order import Order

DELIVERY_FEE = 250
FREE_DELIVERY_FROM = 2500
TUESDAY = 1


class PromotionRefused(Exception):
    pass


class Promotion(Protocol):
    def discount(self, order: Order) -> int: ...


@dataclass(frozen=True)
class StudentDiscount:
    percent: int

    def discount(self, order: Order) -> int:
        if not order.customer.is_student:
            raise PromotionRefused("Code réservé aux étudiants")
        return order.subtotal * self.percent // 100


@dataclass(frozen=True)
class HappyHour:
    percent: int
    hour: int

    def discount(self, order: Order) -> int:
        if order.placed_at.hour != self.hour:
            return 0
        return order.subtotal * self.percent // 100


class ThreeForTwo:
    def discount(self, order: Order) -> int:
        prices = sorted(line.pizza.price for line in order.lines for _ in range(line.quantity))
        return sum(prices[: len(prices) // 3])


@dataclass(frozen=True)
class TuesdayDeal:
    per_pizza: int

    def discount(self, order: Order) -> int:
        if order.placed_at.weekday() != TUESDAY:
            return 0
        return min(order.pizza_count * self.per_pizza, order.subtotal)


PROMOTIONS: dict[str, Promotion] = {
    "ETUDIANT": StudentDiscount(percent=20),
    "HAPPYHOUR": HappyHour(percent=10, hour=18),
    "3POUR2": ThreeForTwo(),
    "MARDI": TuesdayDeal(per_pizza=200),
}


@dataclass(frozen=True)
class Total:
    subtotal: int
    discount: int
    delivery_fee: int

    @property
    def amount(self) -> int:
        return self.subtotal - self.discount + self.delivery_fee


def compute_total(order: Order) -> Total:
    discount = 0
    if order.promo_code is not None:
        if order.promo_code not in PROMOTIONS:
            raise PromotionRefused(f"Code inconnu : {order.promo_code}")
        discount = PROMOTIONS[order.promo_code].discount(order)

    delivery_fee = 0 if order.subtotal - discount >= FREE_DELIVERY_FROM else DELIVERY_FEE
    return Total(order.subtotal, discount, delivery_fee)
