from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from pronto.menu import Pizza


class OrderStatus(StrEnum):
    PLACED = "validée"
    IN_OVEN = "au four"
    OUT_FOR_DELIVERY = "en livraison"
    DELIVERED = "livrée"


NEXT_STATUS = {
    OrderStatus.PLACED: OrderStatus.IN_OVEN,
    OrderStatus.IN_OVEN: OrderStatus.OUT_FOR_DELIVERY,
    OrderStatus.OUT_FOR_DELIVERY: OrderStatus.DELIVERED,
}


@dataclass
class Customer:
    name: str
    phone: str
    country: str = "FR"
    is_student: bool = False


@dataclass
class OrderLine:
    pizza: Pizza
    quantity: int

    @property
    def total(self) -> int:
        return self.pizza.price * self.quantity


@dataclass
class Order:
    customer: Customer
    channel: str
    placed_at: datetime
    lines: list[OrderLine] = field(default_factory=list)
    promo_code: str | None = None
    status: OrderStatus = OrderStatus.PLACED
    number: int | None = None

    @property
    def subtotal(self) -> int:
        return sum(line.total for line in self.lines)

    @property
    def pizza_count(self) -> int:
        return sum(line.quantity for line in self.lines)
