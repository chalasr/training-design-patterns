from pronto.countries import kit_for
from pronto.events import OrderStatusChanged
from pronto.notifications import CourierBoard, KitchenScreen, LoyaltyProgram
from pronto.order import OrderStatus
from pronto.pricing import compute_total


class SmsNotifier:
    def __call__(self, event: OrderStatusChanged) -> None:
        order = event.order
        if order.status is OrderStatus.PLACED:
            message = f"Pronto : commande n° {order.number} validée."
        else:
            message = f"Pronto : votre commande n° {order.number} est {order.status}."
        kit_for(order.customer.country).create_sms_gateway().send(order.customer.phone, message)


class KitchenDisplay:
    def __init__(self, screen: KitchenScreen) -> None:
        self.screen = screen

    def __call__(self, event: OrderStatusChanged) -> None:
        order = event.order
        if order.status is OrderStatus.PLACED:
            self.screen.display(f"#{order.number} : {order.pizza_count} pizza(s)")
        elif order.status is OrderStatus.IN_OVEN:
            self.screen.display(f"#{order.number} au four")


class LoyaltyRewarder:
    def __init__(self, loyalty: LoyaltyProgram) -> None:
        self.loyalty = loyalty

    def __call__(self, event: OrderStatusChanged) -> None:
        order = event.order
        if order.status is OrderStatus.DELIVERED:
            self.loyalty.add_points(order.customer.phone, compute_total(order).amount // 100)


class CourierDispatch:
    def __init__(self, board: CourierBoard) -> None:
        self.board = board

    def __call__(self, event: OrderStatusChanged) -> None:
        order = event.order
        if order.status is OrderStatus.OUT_FOR_DELIVERY:
            self.board.post(f"#{order.number} à livrer : {order.customer.name}")
