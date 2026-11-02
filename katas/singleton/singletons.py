from dataclasses import dataclass
from typing import Any


@dataclass
class AppConfig:
    currency: str = "EUR"
    timezone: str = "Europe/Paris"


class ConfigWithNew(AppConfig):
    """Singleton par __new__."""

    def __new__(cls) -> "ConfigWithNew":
        raise NotImplementedError


class SingletonMeta(type):
    """Métaclasse qui rend unique chaque classe qui l'utilise."""

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class ConfigWithMetaclass(AppConfig, metaclass=SingletonMeta):
    pass


def get_config() -> AppConfig:
    """Accès à une instance unique d'AppConfig, sans toucher à la classe."""
    raise NotImplementedError
