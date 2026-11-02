import copy
from datetime import datetime

from pronto.order import Order


def reorder(order: Order, now: datetime) -> Order:
    """« Recommander » : une nouvelle commande, identique à une commande passée."""
    new_order = copy.copy(order)
    new_order.number = None
    new_order.placed_at = now
    return new_order
