from datetime import datetime
from typing import Self

from pronto.menu import menu_pizza
from pronto.order import Customer, Order, OrderLine


class OrderBuilder:
    def __init__(self) -> None:
        self._customer = Customer("Alice", "+33612345678")
        self._lines: list[OrderLine] = []
        self._promo_code: str | None = None
        self._placed_at = datetime(2026, 11, 3, 12, 0)

    def with_pizza(self, name: str, quantity: int = 1) -> Self:
        self._lines.append(OrderLine(menu_pizza(name), quantity))
        return self

    def with_promo_code(self, code: str) -> Self:
        self._promo_code = code
        return self

    def for_a_student(self) -> Self:
        self._customer.is_student = True
        return self

    def placed_at(self, when: datetime) -> Self:
        self._placed_at = when
        return self

    def build(self) -> Order:
        return Order(self._customer, "web", self._placed_at, self._lines, self._promo_code)


def an_order() -> OrderBuilder:
    return OrderBuilder()
