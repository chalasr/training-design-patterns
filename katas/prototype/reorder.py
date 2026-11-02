import copy
from dataclasses import replace
from datetime import datetime

from pronto.order import Order, OrderStatus


def reorder(order: Order, now: datetime) -> Order:
    """« Recommander » : une nouvelle commande, identique à une commande passée."""
    return replace(
        order,
        lines=copy.deepcopy(order.lines),
        number=None,
        placed_at=now,
        status=OrderStatus.PLACED,
    )
