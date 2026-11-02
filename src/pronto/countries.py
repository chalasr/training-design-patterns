import re
from dataclasses import dataclass
from typing import Protocol

from pronto.notifications import OUTBOX, SentSms


class UnservedCountry(Exception):
    pass


class PhoneValidator(Protocol):
    def is_valid(self, phone: str) -> bool: ...


class SmsGateway(Protocol):
    def send(self, phone: str, message: str) -> None: ...


class InvoiceFormatter(Protocol):
    def header(self) -> str: ...

    def vat_rate(self) -> int: ...


class CountryKit(Protocol):
    def create_phone_validator(self) -> PhoneValidator: ...

    def create_sms_gateway(self) -> SmsGateway: ...

    def create_invoice_formatter(self) -> InvoiceFormatter: ...


@dataclass(frozen=True)
class RegexPhoneValidator:
    pattern: str

    def is_valid(self, phone: str) -> bool:
        return re.fullmatch(self.pattern, phone) is not None


class SmsFranceGateway:
    def send(self, phone: str, message: str) -> None:
        OUTBOX.sent.append(SentSms("SmsFrance", phone, message))


class BelSmsGateway:
    def send(self, phone: str, message: str) -> None:
        OUTBOX.sent.append(SentSms("BelSms", phone, message))


class LuxSmsGateway:
    def send(self, phone: str, message: str) -> None:
        OUTBOX.sent.append(SentSms("LuxSms", phone, message))


@dataclass(frozen=True)
class CompanyInvoice:
    company: str
    rate: int

    def header(self) -> str:
        return self.company

    def vat_rate(self) -> int:
        return self.rate


class FranceKit:
    def create_phone_validator(self) -> PhoneValidator:
        return RegexPhoneValidator(r"\+33[1-9]\d{8}")

    def create_sms_gateway(self) -> SmsGateway:
        return SmsFranceGateway()

    def create_invoice_formatter(self) -> InvoiceFormatter:
        return CompanyInvoice("Pronto France SAS - 12 rue de la Pâte, 75011 Paris", 10)


class BelgiumKit:
    def create_phone_validator(self) -> PhoneValidator:
        return RegexPhoneValidator(r"\+32\d{8,9}")

    def create_sms_gateway(self) -> SmsGateway:
        return BelSmsGateway()

    def create_invoice_formatter(self) -> InvoiceFormatter:
        return CompanyInvoice("Pronto Belgique SRL - 4 rue de la Mozzarella, 1000 Bruxelles", 6)


class LuxembourgKit:
    def create_phone_validator(self) -> PhoneValidator:
        return RegexPhoneValidator(r"\+352\d{6,9}")

    def create_sms_gateway(self) -> SmsGateway:
        return LuxSmsGateway()

    def create_invoice_formatter(self) -> InvoiceFormatter:
        return CompanyInvoice("Pronto Luxembourg SARL - 2 place de la Burrata, 1111 Luxembourg", 3)


KITS: dict[str, CountryKit] = {"FR": FranceKit(), "BE": BelgiumKit(), "LU": LuxembourgKit()}


def kit_for(country: str) -> CountryKit:
    if country not in KITS:
        raise UnservedCountry(f"Pays non desservi : {country}")
    return KITS[country]
