import sqlite3


class Database:
    def __init__(self, path: str) -> None:
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS orders ("
            "number INTEGER PRIMARY KEY AUTOINCREMENT, data BLOB NOT NULL)"
        )
