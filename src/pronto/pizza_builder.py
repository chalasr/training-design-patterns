from typing import Self

from pronto.menu import BASES, DOUGHS, MAX_TOPPINGS, SIZE_PRICES, TOPPING_PRICE, Pizza


class InvalidPizza(ValueError):
    pass


class PizzaBuilder:
    def __init__(self) -> None:
        self._size: str | None = None
        self._dough = "classique"
        self._base = "tomate"
        self._toppings: list[str] = []
        self._left: list[str] = []
        self._right: list[str] = []

    def size(self, size: str) -> Self:
        self._size = size
        return self

    def dough(self, dough: str) -> Self:
        self._dough = dough
        return self

    def base(self, base: str) -> Self:
        self._base = base
        return self

    def topping(self, *toppings: str) -> Self:
        self._toppings.extend(toppings)
        return self

    def left(self, *toppings: str) -> Self:
        self._left.extend(toppings)
        return self

    def right(self, *toppings: str) -> Self:
        self._right.extend(toppings)
        return self

    def build(self) -> Pizza:
        if self._size is None:
            raise InvalidPizza("La taille est obligatoire")
        if self._size not in SIZE_PRICES:
            raise InvalidPizza(f"Taille inconnue : {self._size}")
        if self._dough not in DOUGHS:
            raise InvalidPizza(f"Pâte inconnue : {self._dough}")
        if self._base not in BASES:
            raise InvalidPizza(f"Base inconnue : {self._base}")
        count = len(self._toppings) + len(self._left) + len(self._right)
        if count > MAX_TOPPINGS:
            raise InvalidPizza(f"Pas plus de {MAX_TOPPINGS} garnitures")
        if self._left or self._right:
            if self._size != "L":
                raise InvalidPizza("Moitié-moitié en taille L uniquement")
            if not (self._left and self._right):
                raise InvalidPizza("Chaque moitié a au moins une garniture")
        return Pizza(
            name="sur-mesure",
            price=SIZE_PRICES[self._size] + count * TOPPING_PRICE,
            size=self._size,
            dough=self._dough,
            base=self._base,
            toppings=list(self._toppings),
            left_toppings=list(self._left),
            right_toppings=list(self._right),
        )
