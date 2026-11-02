from datetime import datetime

import pytest

from pronto.countries import BelgiumKit, FranceKit, LuxembourgKit, UnservedCountry, kit_for

NOON = datetime(2026, 11, 3, 12, 0)


@pytest.mark.parametrize(
    ("kit", "phone", "foreign_phone", "provider", "company"),
    [
        (FranceKit(), "+33612345678", "+32470123456", "SmsFrance", "Pronto France"),
        (BelgiumKit(), "+32470123456", "+33612345678", "BelSms", "Pronto Belgique"),
        (LuxembourgKit(), "+352621123456", "+33612345678", "LuxSms", "Pronto Luxembourg"),
    ],
)
def test_a_kit_creates_products_of_a_single_country(
    kit, phone, foreign_phone, provider, company, outbox
):
    validator = kit.create_phone_validator()
    kit.create_sms_gateway().send(phone, "Bonjour")

    assert validator.is_valid(phone)
    assert not validator.is_valid(foreign_phone)
    assert outbox.sent[0].provider == provider
    assert kit.create_invoice_formatter().header().startswith(company)


def test_a_luxembourg_order_is_validated_texted_and_invoiced_in_luxembourg(
    receive_order, invoice, outbox
):
    order = receive_order(
        "web",
        {
            "customer": {"name": "Léa", "phone": "+352621123456", "country": "LU"},
            "items": [{"pizza": "margherita"}],
        },
        NOON,
    )

    assert outbox.sent[0].provider == "LuxSms"
    assert invoice(order).splitlines()[0].startswith("Pronto Luxembourg SARL")
    assert invoice(order).splitlines()[-1] == "Total TTC : 11,50 € (dont TVA 3 % : 0,33 €)"


def test_an_unserved_country_is_refused():
    with pytest.raises(UnservedCountry):
        kit_for("DE")
