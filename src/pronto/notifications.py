from dataclasses import dataclass, field


@dataclass
class SentSms:
    provider: str
    phone: str
    message: str


@dataclass
class SmsOutbox:
    """Simule les passerelles SMS : on garde les messages au lieu de les envoyer."""

    sent: list[SentSms] = field(default_factory=list)


OUTBOX = SmsOutbox()


@dataclass
class KitchenScreen:
    lines: list[str] = field(default_factory=list)

    def display(self, text: str) -> None:
        self.lines.append(text)


@dataclass
class LoyaltyProgram:
    points: dict[str, int] = field(default_factory=dict)

    def add_points(self, phone: str, points: int) -> None:
        self.points[phone] = self.points.get(phone, 0) + points


KITCHEN_SCREEN = KitchenScreen()
LOYALTY = LoyaltyProgram()
