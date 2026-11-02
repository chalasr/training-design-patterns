from datetime import datetime

from pronto.events import OrderStatusChanged, Publisher
from pronto.order import Customer, Order

NOON = datetime(2026, 11, 3, 12, 0)


def an_event() -> OrderStatusChanged:
    return OrderStatusChanged(Order(Customer("Alice", "+33612345678"), "web", NOON))


def test_every_subscriber_is_notified_in_subscription_order():
    received = []
    publisher = Publisher()
    publisher.subscribe(lambda event: received.append("sms"))
    publisher.subscribe(lambda event: received.append("cuisine"))

    publisher.notify(an_event())

    assert received == ["sms", "cuisine"]


def test_a_failing_subscriber_does_not_block_the_others(caplog):
    received = []

    def broken(event: OrderStatusChanged) -> None:
        raise ConnectionError("passerelle injoignable")

    publisher = Publisher()
    publisher.subscribe(broken)
    publisher.subscribe(lambda event: received.append(event))

    publisher.notify(an_event())

    assert len(received) == 1
    assert "passerelle injoignable" in caplog.text


def test_couriers_are_called_when_an_order_leaves_the_oven(app, receive_order, service):
    order = receive_order("phone", "Bob;+33698765432;FR\n1 calzone", NOON)
    service.advance(order.number)
    assert app.courier_board.lines == []

    service.advance(order.number)

    assert app.courier_board.lines == [f"#{order.number} à livrer : Bob"]
