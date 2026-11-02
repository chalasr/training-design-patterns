import copy
from dataclasses import dataclass, field

SIZE_PRICES = {"S": 800, "M": 1000, "L": 1300}
TOPPING_PRICE = 150
MAX_TOPPINGS = 6
DOUGHS = ("classique", "fine", "complete")
BASES = ("tomate", "creme")


@dataclass
class Pizza:
    name: str
    price: int
    size: str = "M"
    dough: str = "classique"
    base: str = "tomate"
    toppings: list[str] = field(default_factory=list)
    left_toppings: list[str] = field(default_factory=list)
    right_toppings: list[str] = field(default_factory=list)


MENU: dict[str, Pizza] = {
    "margherita": Pizza("margherita", 900, toppings=["mozzarella", "basilic"]),
    "reine": Pizza("reine", 1100, toppings=["mozzarella", "jambon", "champignons"]),
    "quatre-fromages": Pizza(
        "quatre-fromages",
        1250,
        base="creme",
        toppings=["mozzarella", "gorgonzola", "chevre", "parmesan"],
    ),
    "calzone": Pizza("calzone", 1200, toppings=["mozzarella", "jambon", "oeuf"]),
}


def menu_pizza(name: str) -> Pizza:
    if name not in MENU:
        raise ValueError(f"Pizza inconnue : {name}")
    return copy.deepcopy(MENU[name])
