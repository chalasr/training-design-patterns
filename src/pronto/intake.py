from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol

from pronto.countries import UnservedCountry, kit_for
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


@dataclass(frozen=True)
class ReceivedOrder:
    customer: Customer
    lines: list[OrderLine]
    promo_code: str | None = None


class OrderReader(Protocol):
    def read(self, payload: Any) -> ReceivedOrder: ...


class WebReader:
    def read(self, payload: Any) -> ReceivedOrder:
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
        return ReceivedOrder(customer, lines, payload.get("promo_code"))


class PhoneReader:
    def read(self, payload: Any) -> ReceivedOrder:
        # Saisie de l'employé : "Alice;+33612345678;FR" puis une ligne par pizza, "2 reine"
        header, *rows = [row.strip() for row in payload.strip().splitlines()]
        name, phone, country = header.split(";")
        lines = []
        for row in rows:
            quantity, pizza_name = row.split(" ", 1)
            lines.append(OrderLine(menu_pizza(pizza_name), int(quantity)))
        return ReceivedOrder(Customer(name, phone, country), lines)


class PartnerReader:
    def read(self, payload: Any) -> ReceivedOrder:
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
        return ReceivedOrder(customer, lines, payload.get("voucher"))


class KioskReader:
    def read(self, payload: Any) -> ReceivedOrder:
        counts = Counter(payload["pizzas"])
        lines = [OrderLine(menu_pizza(name), quantity) for name, quantity in counts.items()]
        return ReceivedOrder(Customer("Client borne", payload["phone"], "FR"), lines)


class OrderIntake(ABC):
    channel: str

    def __init__(self, service: OrderService) -> None:
        self.service = service

    @abstractmethod
    def create_reader(self) -> OrderReader: ...

    def receive(self, payload: Any, now: datetime) -> Order:
        received = self.create_reader().read(payload)
        customer = received.customer
        if not received.lines:
            raise InvalidOrder("Une commande contient au moins une pizza")
        try:
            kit = kit_for(customer.country)
        except UnservedCountry as error:
            raise InvalidOrder(str(error)) from error
        if not kit.create_phone_validator().is_valid(customer.phone):
            raise InvalidOrder(f"Numéro invalide : {customer.phone}")

        order = Order(customer, self.channel, now, received.lines, received.promo_code)
        return self.service.place(order)


class WebIntake(OrderIntake):
    channel = "web"

    def create_reader(self) -> OrderReader:
        return WebReader()


class PhoneIntake(OrderIntake):
    channel = "phone"

    def create_reader(self) -> OrderReader:
        return PhoneReader()


class PartnerIntake(OrderIntake):
    channel = "partner"

    def create_reader(self) -> OrderReader:
        return PartnerReader()


class KioskIntake(OrderIntake):
    channel = "kiosk"

    def create_reader(self) -> OrderReader:
        return KioskReader()
