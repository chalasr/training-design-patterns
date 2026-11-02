import logging
from collections.abc import Callable
from dataclasses import dataclass

from pronto.order import Order

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OrderStatusChanged:
    order: Order


type Subscriber = Callable[[OrderStatusChanged], None]


class Publisher:
    def __init__(self) -> None:
        self._subscribers: list[Subscriber] = []

    def subscribe(self, subscriber: Subscriber) -> None:
        self._subscribers.append(subscriber)

    def notify(self, event: OrderStatusChanged) -> None:
        for subscriber in self._subscribers:
            try:
                subscriber(event)
            except Exception:
                logger.exception("L'abonné %r a échoué sur %r", subscriber, event)
