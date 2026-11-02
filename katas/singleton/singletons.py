import functools
import threading
from dataclasses import dataclass
from typing import Any


@dataclass
class AppConfig:
    currency: str = "EUR"
    timezone: str = "Europe/Paris"


class ConfigWithNew(AppConfig):
    """Singleton par __new__."""

    _instance: "ConfigWithNew | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "ConfigWithNew":
        with cls._lock:
            if cls._instance is None:
                instance = super().__new__(cls)
                AppConfig.__init__(instance)
                cls._instance = instance
        return cls._instance

    def __init__(self) -> None:
        # AppConfig.__init__ remettrait les réglages par défaut à chaque appel.
        pass


class SingletonMeta(type):
    """Métaclasse qui rend unique chaque classe qui l'utilise."""

    _instances: dict[type, Any] = {}
    _lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with SingletonMeta._lock:
            if cls not in SingletonMeta._instances:
                SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)
        return SingletonMeta._instances[cls]


class ConfigWithMetaclass(AppConfig, metaclass=SingletonMeta):
    pass


@functools.cache
def get_config() -> AppConfig:
    """Accès à une instance unique d'AppConfig, sans toucher à la classe."""
    return AppConfig()
