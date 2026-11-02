"""Démonstration formateur : un pool de connexions aux terminaux de paiement.

python demos/object_pool.py
"""

import queue
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager

CONNECTION_DELAY = 0.5


class PaymentTerminal:
    created = 0

    def __init__(self) -> None:
        time.sleep(CONNECTION_DELAY)
        PaymentTerminal.created += 1
        self.id = PaymentTerminal.created
        self.pending_amount: int | None = None

    def charge(self, cents: int) -> str:
        self.pending_amount = cents
        receipt = f"terminal {self.id} : {cents / 100:.2f} € débités"
        self.pending_amount = None
        return receipt

    def reset(self) -> None:
        self.pending_amount = None


class PoolExhausted(Exception):
    pass


class TerminalPool:
    def __init__(self, size: int) -> None:
        self._idle: queue.Queue[PaymentTerminal] = queue.Queue()
        for _ in range(size):
            self._idle.put(PaymentTerminal())

    @contextmanager
    def terminal(self, timeout: float = 1.0) -> Iterator[PaymentTerminal]:
        try:
            terminal = self._idle.get(timeout=timeout)
        except queue.Empty:
            raise PoolExhausted from None
        try:
            yield terminal
        finally:
            terminal.reset()
            self._idle.put(terminal)


def without_pool(payments: int) -> None:
    start = time.perf_counter()
    for cents in range(payments):
        PaymentTerminal().charge(1000 + cents)
    print(f"sans pool : {payments} paiements en {time.perf_counter() - start:.1f} s")


def with_pool(payments: int) -> None:
    start = time.perf_counter()
    pool = TerminalPool(size=2)
    for cents in range(payments):
        with pool.terminal() as terminal:
            terminal.charge(1000 + cents)
    elapsed = time.perf_counter() - start
    print(f"avec pool (création comprise) : {payments} paiements en {elapsed:.1f} s")


def exhaustion() -> None:
    pool = TerminalPool(size=1)
    held = threading.Event()
    release = threading.Event()

    def slow_payment() -> None:
        with pool.terminal():
            held.set()
            release.wait()

    worker = threading.Thread(target=slow_payment)
    worker.start()
    held.wait()
    try:
        with pool.terminal(timeout=0.2):
            pass
    except PoolExhausted:
        print("pool épuisé : le deuxième paiement attend un terminal libre")
    release.set()
    worker.join()


if __name__ == "__main__":
    without_pool(6)
    with_pool(6)
    exhaustion()
