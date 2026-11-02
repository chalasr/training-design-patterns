from pronto.countries import kit_for
from pronto.notifications import KITCHEN_SCREEN, LOYALTY
from pronto.order import NEXT_STATUS, Order, OrderStatus
from pronto.pricing import compute_total
from pronto.repository import OrderRepository


class OrderAlreadyDelivered(Exception):
    pass


class OrderService:
    def __init__(self, orders: OrderRepository) -> None:
        self.orders = orders

    def place(self, order: Order) -> Order:
        compute_total(order)
        self.orders.add(order)
        KITCHEN_SCREEN.display(f"#{order.number} : {order.pizza_count} pizza(s)")
        kit_for(order.customer.country).create_sms_gateway().send(
            order.customer.phone, f"Pronto : commande n° {order.number} validée."
        )
        return order

    def advance(self, number: int) -> Order:
        order = self.orders.get(number)
        if order.status is OrderStatus.DELIVERED:
            raise OrderAlreadyDelivered(number)
        order.status = NEXT_STATUS[order.status]
        self.orders.save(order)

        if order.status is OrderStatus.IN_OVEN:
            KITCHEN_SCREEN.display(f"#{order.number} au four")
        kit_for(order.customer.country).create_sms_gateway().send(
            order.customer.phone, f"Pronto : votre commande n° {order.number} est {order.status}."
        )
        if order.status is OrderStatus.DELIVERED:
            LOYALTY.add_points(order.customer.phone, compute_total(order).amount // 100)
        return order
