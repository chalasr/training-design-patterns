import pytest

from pronto.database import Database
from pronto.intake import OrderIntake
from pronto.invoice import render_invoice
from pronto.notifications import KITCHEN_SCREEN, LOYALTY, OUTBOX
from pronto.repository import OrderRepository
from pronto.service import OrderService


@pytest.fixture(autouse=True)
def fresh_state():
    Database.reset_instance()
    OUTBOX.sent.clear()
    KITCHEN_SCREEN.lines.clear()
    LOYALTY.points.clear()


@pytest.fixture
def receive_order():
    """Le point d'entrée des commandes, quel que soit le canal (les routes de l'application)."""
    return OrderIntake().receive


@pytest.fixture
def service():
    return OrderService()


@pytest.fixture
def orders():
    return OrderRepository()


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
