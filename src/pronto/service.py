from pronto.notifications import KITCHEN_SCREEN, LOYALTY, send_sms
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
        send_sms(
            order.customer.phone,
            f"Pronto : commande n° {order.number} validée.",
            order.customer.country,
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
        send_sms(
            order.customer.phone,
            f"Pronto : votre commande n° {order.number} est {order.status}.",
            order.customer.country,
        )
        if order.status is OrderStatus.DELIVERED:
            LOYALTY.add_points(order.customer.phone, compute_total(order).amount // 100)
        return order
