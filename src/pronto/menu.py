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
    return MENU[name]


def make_custom_pizza(
    size: str,
    dough: str = "classique",
    base: str = "tomate",
    toppings: list[str] | None = None,
    left_toppings: list[str] | None = None,
    right_toppings: list[str] | None = None,
) -> Pizza:
    toppings = toppings or []
    left_toppings = left_toppings or []
    right_toppings = right_toppings or []
    if size not in SIZE_PRICES:
        raise ValueError(f"Taille inconnue : {size}")
    if dough not in DOUGHS:
        raise ValueError(f"Pâte inconnue : {dough}")
    if len(toppings) + len(left_toppings) + len(right_toppings) > MAX_TOPPINGS:
        raise ValueError("Pas plus de 6 garnitures")
    if (left_toppings or right_toppings) and size != "L":
        raise ValueError("Moitié-moitié en taille L uniquement")
    count = len(toppings) + len(left_toppings) + len(right_toppings)
    return Pizza(
        name="sur-mesure",
        price=SIZE_PRICES[size] + count * TOPPING_PRICE,
        size=size,
        dough=dough,
        base=base,
        toppings=toppings,
        left_toppings=left_toppings,
        right_toppings=right_toppings,
    )
