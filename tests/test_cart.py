import pytest

from pronto.cart import Cart, NotInCart


def test_adding_the_same_pizza_twice_increases_its_quantity():
    cart = Cart()
    cart.add("reine")
    cart.add("reine", 2)

    assert cart.quantity_of("reine") == 3
    assert len(cart.lines) == 1


def test_a_pizza_can_be_removed():
    cart = Cart()
    cart.add("reine")
    cart.remove("reine")

    assert cart.lines == []


def test_removing_a_pizza_that_is_not_in_the_cart_fails():
    with pytest.raises(NotInCart):
        Cart().remove("reine")


def test_a_coupon_can_be_applied():
    cart = Cart()
    cart.apply_coupon("ETUDIANT")

    assert cart.promo_code == "ETUDIANT"
