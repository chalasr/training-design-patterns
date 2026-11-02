import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pronto.database import Database
from pronto.events import Publisher
from pronto.intake import (
    InvalidOrder,
    KioskIntake,
    OrderIntake,
    PartnerIntake,
    PhoneIntake,
    WebIntake,
)
from pronto.notifications import CourierBoard, KitchenScreen, LoyaltyProgram
from pronto.order import Order
from pronto.repository import OrderRepository
from pronto.service import OrderService
from pronto.subscribers import CourierDispatch, KitchenDisplay, LoyaltyRewarder, SmsNotifier


@dataclass(frozen=True)
class App:
    database: Database
    orders: OrderRepository
    service: OrderService
    intakes: dict[str, OrderIntake]
    publisher: Publisher
    kitchen_screen: KitchenScreen
    loyalty: LoyaltyProgram
    courier_board: CourierBoard

    def receive_order(self, channel: str, payload: Any, now: datetime) -> Order:
        if channel not in self.intakes:
            raise InvalidOrder(f"Canal inconnu : {channel}")
        return self.intakes[channel].receive(payload, now)


def create_app(database_path: str | None = None) -> App:
    database = Database(database_path or os.environ.get("PRONTO_DATABASE", ":memory:"))
    orders = OrderRepository(database)
    kitchen_screen = KitchenScreen()
    loyalty = LoyaltyProgram()
    courier_board = CourierBoard()
    publisher = Publisher()
    publisher.subscribe(SmsNotifier())
    publisher.subscribe(KitchenDisplay(kitchen_screen))
    publisher.subscribe(LoyaltyRewarder(loyalty))
    publisher.subscribe(CourierDispatch(courier_board))
    service = OrderService(orders, publisher)
    intakes: dict[str, OrderIntake] = {
        intake.channel: intake
        for intake in (
            WebIntake(service),
            PhoneIntake(service),
            PartnerIntake(service),
            KioskIntake(service),
        )
    }
    return App(
        database, orders, service, intakes, publisher, kitchen_screen, loyalty, courier_board
    )
