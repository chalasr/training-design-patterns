import os
import sqlite3


class Database:
    _instance: "Database | None" = None

    def __init__(self, path: str) -> None:
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS orders ("
            "number INTEGER PRIMARY KEY AUTOINCREMENT, data BLOB NOT NULL)"
        )

    @classmethod
    def instance(cls) -> "Database":
        if cls._instance is None:
            cls._instance = cls(os.environ.get("PRONTO_DATABASE", ":memory:"))
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Pour les tests uniquement."""
        cls._instance = None
