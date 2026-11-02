import re
from datetime import datetime
from typing import Any

from pronto.menu import Pizza, make_custom_pizza, menu_pizza
from pronto.order import Customer, Order, OrderLine
from pronto.service import OrderService

PARTNER_SKUS = {
    "PZ-MARG": "margherita",
    "PZ-REINE": "reine",
    "PZ-4FROM": "quatre-fromages",
    "PZ-CALZ": "calzone",
}


class InvalidOrder(Exception):
    pass


class OrderIntake:
    def __init__(self) -> None:
        self.service = OrderService()

    def receive(self, channel: str, payload: Any, now: datetime) -> Order:
        if channel == "web":
            customer = Customer(
                name=payload["customer"]["name"],
                phone=payload["customer"]["phone"],
                country=payload["customer"].get("country", "FR"),
                is_student=payload["customer"].get("is_student", False),
            )
            lines = []
            for item in payload["items"]:
                pizza: Pizza
                if "custom" in item:
                    custom = item["custom"]
                    pizza = make_custom_pizza(
                        custom["size"],
                        custom.get("dough", "classique"),
                        custom.get("base", "tomate"),
                        custom.get("toppings"),
                        custom.get("left"),
                        custom.get("right"),
                    )
                else:
                    pizza = menu_pizza(item["pizza"])
                lines.append(OrderLine(pizza, item.get("quantity", 1)))
            promo_code = payload.get("promo_code")
        elif channel == "phone":
            # Saisie de l'employé : "Alice;+33612345678;FR" puis une ligne par pizza, "2 reine"
            header, *rows = [row.strip() for row in payload.strip().splitlines()]
            name, phone, country = header.split(";")
            customer = Customer(name, phone, country)
            lines = []
            for row in rows:
                quantity, pizza_name = row.split(" ", 1)
                lines.append(OrderLine(menu_pizza(pizza_name), int(quantity)))
            promo_code = None
        elif channel == "partner":
            customer = Customer(
                name=payload["client"]["full_name"],
                phone=payload["client"]["phone_number"],
                country=payload["client"]["country_code"],
            )
            lines = []
            for line in payload["order_lines"]:
                if line["sku"] not in PARTNER_SKUS:
                    raise InvalidOrder(f"Référence partenaire inconnue : {line['sku']}")
                lines.append(OrderLine(menu_pizza(PARTNER_SKUS[line["sku"]]), line["qty"]))
            promo_code = payload.get("voucher")
        else:
            raise InvalidOrder(f"Canal inconnu : {channel}")

        if not lines:
            raise InvalidOrder("Une commande contient au moins une pizza")
        if customer.country == "FR":
            if not re.fullmatch(r"\+33[1-9]\d{8}", customer.phone):
                raise InvalidOrder(f"Numéro français invalide : {customer.phone}")
        elif customer.country == "BE":
            if not re.fullmatch(r"\+32\d{8,9}", customer.phone):
                raise InvalidOrder(f"Numéro belge invalide : {customer.phone}")
        else:
            raise InvalidOrder(f"Pays non desservi : {customer.country}")

        order = Order(customer, channel, now, lines, promo_code)
        return self.service.place(order)
