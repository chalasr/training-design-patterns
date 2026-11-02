from datetime import datetime

import pytest

from pronto.menu import menu_pizza
from pronto.order import Customer, Order, OrderLine
from pronto.pricing import PromotionRefused, compute_total


def order_of(*lines: tuple[str, int], promo_code=None, is_student=False, hour=12) -> Order:
    return Order(
        customer=Customer("Alice", "+33612345678", is_student=is_student),
        channel="web",
        placed_at=datetime(2026, 11, 3, hour, 0),
        lines=[OrderLine(menu_pizza(name), quantity) for name, quantity in lines],
        promo_code=promo_code,
    )


def test_delivery_is_charged_below_25_euros():
    assert compute_total(order_of(("reine", 1))).delivery_fee == 250


def test_delivery_is_free_from_25_euros():
    total = compute_total(order_of(("reine", 1), ("calzone", 1), ("margherita", 1)))

    assert total.delivery_fee == 0


def test_students_get_20_percent_off():
    total = compute_total(order_of(("reine", 2), promo_code="ETUDIANT", is_student=True))

    assert total.discount == 440


def test_the_student_code_is_refused_to_non_students():
    with pytest.raises(PromotionRefused):
        compute_total(order_of(("reine", 2), promo_code="ETUDIANT"))


def test_happy_hour_gives_10_percent_off_between_6_and_7_pm():
    assert compute_total(order_of(("reine", 2), promo_code="HAPPYHOUR", hour=18)).discount == 220
    assert compute_total(order_of(("reine", 2), promo_code="HAPPYHOUR", hour=19)).discount == 0


def test_the_cheapest_pizza_of_every_three_is_free():
    total = compute_total(order_of(("reine", 2), ("margherita", 1), promo_code="3POUR2"))

    assert total.discount == 900


def test_an_unknown_code_is_refused():
    with pytest.raises(PromotionRefused):
        compute_total(order_of(("reine", 1), promo_code="GRATUIT"))
