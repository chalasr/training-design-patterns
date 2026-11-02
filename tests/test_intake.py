from datetime import datetime

import pytest

from pronto.intake import InvalidOrder

NOON = datetime(2026, 11, 3, 12, 0)


def test_each_channel_reads_its_own_format(receive_order):
    web = receive_order(
        "web",
        {"customer": {"name": "Alice", "phone": "+33612345678"}, "items": [{"pizza": "reine"}]},
        NOON,
    )
    phone = receive_order("phone", "Bob;+33698765432;FR\n1 reine", NOON)
    partner = receive_order(
        "partner",
        {
            "client": {"full_name": "Chloé", "phone_number": "+33611111111", "country_code": "FR"},
            "order_lines": [{"sku": "PZ-REINE", "qty": 1}],
        },
        NOON,
    )

    assert [order.channel for order in (web, phone, partner)] == ["web", "phone", "partner"]
    assert [order.customer.name for order in (web, phone, partner)] == ["Alice", "Bob", "Chloé"]
    assert all(order.lines[0].pizza.name == "reine" for order in (web, phone, partner))


def test_a_kiosk_order_groups_identical_pizzas(receive_order):
    order = receive_order(
        "kiosk", {"phone": "+33612345678", "pizzas": ["reine", "reine", "margherita"]}, NOON
    )

    assert order.customer.name == "Client borne"
    assert [(line.pizza.name, line.quantity) for line in order.lines] == [
        ("reine", 2),
        ("margherita", 1),
    ]
    assert order.promo_code is None


def test_an_unknown_channel_is_refused(receive_order):
    with pytest.raises(InvalidOrder):
        receive_order("fax", "2 reine", NOON)
