import pytest

from pronto.menu import make_custom_pizza


def test_a_custom_pizza_costs_its_size_plus_its_toppings():
    pizza = make_custom_pizza("L", "fine", "tomate", ["jambon", "olives"])

    assert pizza.price == 1600


def test_a_custom_pizza_has_at_most_six_toppings():
    with pytest.raises(ValueError):
        make_custom_pizza("M", toppings=["a", "b", "c", "d", "e", "f", "g"])


def test_half_and_half_is_only_for_large_pizzas():
    with pytest.raises(ValueError):
        make_custom_pizza("M", left_toppings=["jambon"], right_toppings=["chevre"])
