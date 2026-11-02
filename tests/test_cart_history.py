from pronto.cart import Cart
from pronto.cart_commands import AddPizza, ApplyCoupon, CartHistory, RemovePizza


def test_adding_a_pizza_can_be_undone():
    cart, history = Cart(), CartHistory()
    history.run(AddPizza(cart, "reine", 2))

    history.undo()

    assert cart.lines == []


def test_undoing_an_addition_keeps_the_pizzas_added_before():
    cart, history = Cart(), CartHistory()
    history.run(AddPizza(cart, "reine", 1))
    history.run(AddPizza(cart, "reine", 2))

    history.undo()

    assert cart.quantity_of("reine") == 1


def test_a_removed_pizza_comes_back_with_its_quantity_on_undo():
    cart, history = Cart(), CartHistory()
    history.run(AddPizza(cart, "reine", 3))
    history.run(RemovePizza(cart, "reine"))

    history.undo()

    assert cart.quantity_of("reine") == 3


def test_undoing_a_coupon_restores_the_previous_one():
    cart, history = Cart(), CartHistory()
    history.run(ApplyCoupon(cart, "ETUDIANT"))
    history.run(ApplyCoupon(cart, "3POUR2"))

    history.undo()

    assert cart.promo_code == "ETUDIANT"


def test_an_undone_action_can_be_redone():
    cart, history = Cart(), CartHistory()
    history.run(AddPizza(cart, "reine", 2))
    history.undo()

    history.redo()

    assert cart.quantity_of("reine") == 2


def test_a_new_action_clears_the_redo_history():
    cart, history = Cart(), CartHistory()
    history.run(AddPizza(cart, "reine"))
    history.undo()
    history.run(AddPizza(cart, "margherita"))

    history.redo()

    assert cart.quantity_of("reine") == 0
    assert cart.quantity_of("margherita") == 1
