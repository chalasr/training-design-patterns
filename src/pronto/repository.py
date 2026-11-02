import pickle

from pronto.database import Database
from pronto.order import Order


class OrderNotFound(Exception):
    pass


class OrderRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def add(self, order: Order) -> Order:
        connection = self.database.connection
        cursor = connection.execute("INSERT INTO orders (data) VALUES (?)", (b"",))
        order.number = cursor.lastrowid
        self.save(order)
        return order

    def save(self, order: Order) -> None:
        connection = self.database.connection
        connection.execute(
            "UPDATE orders SET data = ? WHERE number = ?", (pickle.dumps(order), order.number)
        )
        connection.commit()

    def get(self, number: int) -> Order:
        row = self.database.connection.execute(
            "SELECT data FROM orders WHERE number = ?", (number,)
        ).fetchone()
        if row is None:
            raise OrderNotFound(number)
        order: Order = pickle.loads(row[0])
        return order

    def count(self) -> int:
        row = self.database.connection.execute("SELECT COUNT(*) FROM orders").fetchone()
        return int(row[0])
