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


def send_sms(phone: str, message: str, country: str) -> None:
    if country == "FR":
        if not phone.startswith("+33"):
            raise ValueError(f"Numéro français invalide : {phone}")
        OUTBOX.sent.append(SentSms("SmsFrance", phone, message))
    elif country == "BE":
        if not phone.startswith("+32"):
            raise ValueError(f"Numéro belge invalide : {phone}")
        OUTBOX.sent.append(SentSms("BelSms", phone, message))
    else:
        raise ValueError(f"Pays non desservi : {country}")


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
