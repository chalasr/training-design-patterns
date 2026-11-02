"""Le filet de sécurité : ce fichier ne change à aucune étape."""

from datetime import datetime

import pytest

from pronto.intake import InvalidOrder
from pronto.order import OrderStatus

NOON = datetime(2026, 11, 3, 12, 0)


def test_a_web_order_goes_from_placed_to_delivered(
    receive_order, service, orders, outbox, kitchen_screen, loyalty
):
    order = receive_order(
        "web",
        {
            "customer": {"name": "Alice", "phone": "+33612345678"},
            "items": [{"pizza": "reine", "quantity": 2}, {"pizza": "margherita"}],
        },
        NOON,
    )
    for _ in range(3):
        service.advance(order.number)

    assert orders.get(order.number).status is OrderStatus.DELIVERED
    assert [sms.message for sms in outbox.sent] == [
        f"Pronto : commande n° {order.number} validée.",
        f"Pronto : votre commande n° {order.number} est au four.",
        f"Pronto : votre commande n° {order.number} est en livraison.",
        f"Pronto : votre commande n° {order.number} est livrée.",
    ]
    assert kitchen_screen.lines == [f"#{order.number} : 3 pizza(s)", f"#{order.number} au four"]
    assert loyalty.points == {"+33612345678": 31}


def test_a_phone_order_is_numbered_and_invoiced(receive_order, invoice):
    order = receive_order("phone", "Bob;+33698765432;FR\n1 calzone\n1 margherita", NOON)

    assert order.number == 1
    assert invoice(order) == "\n".join(
        [
            "Pronto France SAS - 12 rue de la Pâte, 75011 Paris",
            "Commande n° 1",
            "1 x calzone : 12,00 €",
            "1 x margherita : 9,00 €",
            "Livraison : 2,50 €",
            "Total TTC : 23,50 € (dont TVA 10 % : 2,13 €)",
        ]
    )


def test_a_partner_order_from_belgium_is_invoiced_in_belgium(receive_order, invoice, outbox):
    order = receive_order(
        "partner",
        {
            "client": {"full_name": "Chloé", "phone_number": "+32470123456", "country_code": "BE"},
            "order_lines": [{"sku": "PZ-4FROM", "qty": 3}],
            "voucher": "3POUR2",
        },
        NOON,
    )

    assert outbox.sent[0].provider == "BelSms"
    assert invoice(order).splitlines()[0].startswith("Pronto Belgique SRL")
    assert invoice(order).splitlines()[-1] == "Total TTC : 25,00 € (dont TVA 6 % : 1,41 €)"


def test_an_invalid_phone_number_is_refused(receive_order, orders):
    with pytest.raises(InvalidOrder):
        receive_order("phone", "Bob;0698765432;FR\n1 calzone", NOON)

    assert orders.count() == 0
