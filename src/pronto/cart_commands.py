from typing import Protocol

from pronto.cart import Cart


class CartCommand(Protocol):
    def execute(self) -> None: ...

    def undo(self) -> None: ...


class AddPizza:
    def __init__(self, cart: Cart, pizza_name: str, quantity: int = 1) -> None:
        self.cart = cart
        self.pizza_name = pizza_name
        self.quantity = quantity

    def execute(self) -> None:
        self.cart.add(self.pizza_name, self.quantity)

    def undo(self) -> None:
        self.cart.withdraw(self.pizza_name, self.quantity)


class RemovePizza:
    def __init__(self, cart: Cart, pizza_name: str) -> None:
        self.cart = cart
        self.pizza_name = pizza_name
        self.removed_quantity = 0

    def execute(self) -> None:
        self.removed_quantity = self.cart.quantity_of(self.pizza_name)
        self.cart.remove(self.pizza_name)

    def undo(self) -> None:
        self.cart.add(self.pizza_name, self.removed_quantity)


class ApplyCoupon:
    def __init__(self, cart: Cart, code: str) -> None:
        self.cart = cart
        self.code = code
        self.previous_code: str | None = None

    def execute(self) -> None:
        self.previous_code = self.cart.promo_code
        self.cart.apply_coupon(self.code)

    def undo(self) -> None:
        self.cart.apply_coupon(self.previous_code)


class CartHistory:
    def __init__(self) -> None:
        self._done: list[CartCommand] = []
        self._undone: list[CartCommand] = []

    def run(self, command: CartCommand) -> None:
        command.execute()
        self._done.append(command)
        self._undone.clear()

    def undo(self) -> None:
        if self._done:
            command = self._done.pop()
            command.undo()
            self._undone.append(command)

    def redo(self) -> None:
        if self._undone:
            command = self._undone.pop()
            command.execute()
            self._done.append(command)
