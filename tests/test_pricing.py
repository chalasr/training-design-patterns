from datetime import datetime

import pytest

from pronto.pricing import PromotionRefused, compute_total
from tests.builders import an_order

SIX_PM = datetime(2026, 11, 3, 18, 0)
SEVEN_PM = datetime(2026, 11, 3, 19, 0)


def test_delivery_is_charged_below_25_euros():
    assert compute_total(an_order().with_pizza("reine").build()).delivery_fee == 250


def test_delivery_is_free_from_25_euros():
    order = an_order().with_pizza("reine").with_pizza("calzone").with_pizza("margherita").build()

    assert compute_total(order).delivery_fee == 0


def test_students_get_20_percent_off():
    order = an_order().with_pizza("reine", 2).with_promo_code("ETUDIANT").for_a_student().build()

    assert compute_total(order).discount == 440


def test_the_student_code_is_refused_to_non_students():
    with pytest.raises(PromotionRefused):
        compute_total(an_order().with_pizza("reine", 2).with_promo_code("ETUDIANT").build())


def test_happy_hour_gives_10_percent_off_between_6_and_7_pm():
    happy = an_order().with_pizza("reine", 2).with_promo_code("HAPPYHOUR")

    assert compute_total(happy.placed_at(SIX_PM).build()).discount == 220
    assert compute_total(happy.placed_at(SEVEN_PM).build()).discount == 0


def test_the_cheapest_pizza_of_every_three_is_free():
    order = (
        an_order().with_pizza("reine", 2).with_pizza("margherita").with_promo_code("3POUR2").build()
    )

    assert compute_total(order).discount == 900


def test_an_unknown_code_is_refused():
    with pytest.raises(PromotionRefused):
        compute_total(an_order().with_pizza("reine").with_promo_code("GRATUIT").build())


TUESDAY_NOON = datetime(2026, 11, 3, 12, 0)
WEDNESDAY_NOON = datetime(2026, 11, 4, 12, 0)


def test_on_tuesdays_each_pizza_is_2_euros_off():
    order = an_order().with_pizza("reine", 2).with_promo_code("MARDI").placed_at(TUESDAY_NOON)

    assert compute_total(order.build()).discount == 400


def test_the_tuesday_code_gives_nothing_on_other_days():
    order = an_order().with_pizza("reine", 2).with_promo_code("MARDI").placed_at(WEDNESDAY_NOON)

    assert compute_total(order.build()).discount == 0
