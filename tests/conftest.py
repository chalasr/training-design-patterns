import pytest

from pronto.app import App, create_app
from pronto.invoice import render_invoice
from pronto.notifications import KITCHEN_SCREEN, LOYALTY, OUTBOX


@pytest.fixture(autouse=True)
def fresh_notifications():
    OUTBOX.sent.clear()
    KITCHEN_SCREEN.lines.clear()
    LOYALTY.points.clear()


@pytest.fixture
def app() -> App:
    return create_app(":memory:")


@pytest.fixture
def receive_order(app):
    """Le point d'entrée des commandes, quel que soit le canal (les routes de l'application)."""
    return app.intake.receive


@pytest.fixture
def service(app):
    return app.service


@pytest.fixture
def orders(app):
    return app.orders


@pytest.fixture
def invoice():
    return render_invoice


@pytest.fixture
def outbox():
    return OUTBOX


@pytest.fixture
def kitchen_screen():
    return KITCHEN_SCREEN


@pytest.fixture
def loyalty():
    return LOYALTY
