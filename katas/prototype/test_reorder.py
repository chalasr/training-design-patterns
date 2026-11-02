from datetime import datetime

from katas.prototype.reorder import reorder
from pronto.menu import MENU, menu_pizza
from pronto.order import Customer, Order, OrderLine, OrderStatus

YESTERDAY = datetime(2026, 11, 2, 20, 0)
NOW = datetime(2026, 11, 3, 20, 0)


def delivered_order() -> Order:
    return Order(
        customer=Customer("Alice", "+33612345678"),
        channel="web",
        placed_at=YESTERDAY,
        lines=[OrderLine(menu_pizza("reine"), 2)],
        status=OrderStatus.DELIVERED,
        number=42,
    )


def test_a_reordered_order_is_a_new_placed_order():
    new_order = reorder(delivered_order(), NOW)

    assert new_order.number is None
    assert new_order.placed_at == NOW
    assert new_order.status is OrderStatus.PLACED


def test_changing_a_reordered_order_does_not_change_the_original():
    original = delivered_order()
    new_order = reorder(original, NOW)

    new_order.lines.append(OrderLine(menu_pizza("margherita"), 1))
    new_order.lines[0].quantity = 5

    assert len(original.lines) == 1
    assert original.lines[0].quantity == 2


def test_customising_a_pizza_from_the_menu_does_not_change_the_menu():
    pizza = menu_pizza("reine")
    pizza.toppings.append("olives")

    assert MENU["reine"].toppings == ["mozzarella", "jambon", "champignons"]
