from pronto.events import OrderStatusChanged, Publisher
from pronto.order import NEXT_STATUS, Order, OrderStatus
from pronto.pricing import compute_total
from pronto.repository import OrderRepository


class OrderAlreadyDelivered(Exception):
    pass


class OrderService:
    def __init__(self, orders: OrderRepository, publisher: Publisher) -> None:
        self.orders = orders
        self.publisher = publisher

    def place(self, order: Order) -> Order:
        compute_total(order)
        self.orders.add(order)
        self.publisher.notify(OrderStatusChanged(order))
        return order

    def advance(self, number: int) -> Order:
        order = self.orders.get(number)
        if order.status is OrderStatus.DELIVERED:
            raise OrderAlreadyDelivered(number)
        order.status = NEXT_STATUS[order.status]
        self.orders.save(order)
        self.publisher.notify(OrderStatusChanged(order))
        return order
