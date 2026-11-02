from dataclasses import dataclass, field

from pronto.menu import menu_pizza
from pronto.order import OrderLine


class NotInCart(Exception):
    pass


@dataclass
class Cart:
    """Le panier du site, gardé en session jusqu'à la validation."""

    lines: list[OrderLine] = field(default_factory=list)
    promo_code: str | None = None

    def add(self, pizza_name: str, quantity: int = 1) -> None:
        for line in self.lines:
            if line.pizza.name == pizza_name:
                line.quantity += quantity
                return
        self.lines.append(OrderLine(menu_pizza(pizza_name), quantity))

    def remove(self, pizza_name: str) -> None:
        for line in self.lines:
            if line.pizza.name == pizza_name:
                self.lines.remove(line)
                return
        raise NotInCart(pizza_name)

    def withdraw(self, pizza_name: str, quantity: int) -> None:
        for line in self.lines:
            if line.pizza.name == pizza_name:
                line.quantity -= quantity
                if line.quantity <= 0:
                    self.lines.remove(line)
                return
        raise NotInCart(pizza_name)

    def apply_coupon(self, code: str | None) -> None:
        self.promo_code = code

    def quantity_of(self, pizza_name: str) -> int:
        return sum(line.quantity for line in self.lines if line.pizza.name == pizza_name)
