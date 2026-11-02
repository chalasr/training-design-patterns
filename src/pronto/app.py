import os
from dataclasses import dataclass

from pronto.database import Database
from pronto.intake import OrderIntake
from pronto.repository import OrderRepository
from pronto.service import OrderService


@dataclass(frozen=True)
class App:
    database: Database
    orders: OrderRepository
    service: OrderService
    intake: OrderIntake


def create_app(database_path: str | None = None) -> App:
    database = Database(database_path or os.environ.get("PRONTO_DATABASE", ":memory:"))
    orders = OrderRepository(database)
    service = OrderService(orders)
    return App(database, orders, service, OrderIntake(service))
