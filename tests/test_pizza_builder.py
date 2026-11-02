import pytest

from pronto.pizza_builder import InvalidPizza, PizzaBuilder


def test_a_custom_pizza_costs_its_size_plus_its_toppings():
    pizza = PizzaBuilder().size("L").dough("fine").topping("jambon", "olives").build()

    assert pizza.price == 1600


def test_a_size_is_required():
    with pytest.raises(InvalidPizza):
        PizzaBuilder().topping("jambon").build()


def test_an_unknown_base_is_refused():
    with pytest.raises(InvalidPizza):
        PizzaBuilder().size("M").base("barbecue").build()


def test_a_custom_pizza_has_at_most_six_toppings():
    with pytest.raises(InvalidPizza):
        PizzaBuilder().size("M").topping("a", "b", "c", "d", "e", "f", "g").build()


def test_half_and_half_is_only_for_large_pizzas():
    with pytest.raises(InvalidPizza):
        PizzaBuilder().size("M").left("jambon").right("chevre").build()


def test_each_half_has_at_least_one_topping():
    with pytest.raises(InvalidPizza):
        PizzaBuilder().size("L").left("jambon").build()


def test_a_half_and_half_pizza_counts_the_toppings_of_both_halves():
    pizza = PizzaBuilder().size("L").left("jambon", "olives").right("chevre").build()

    assert pizza.price == 1750
    assert pizza.left_toppings == ["jambon", "olives"]
    assert pizza.right_toppings == ["chevre"]
