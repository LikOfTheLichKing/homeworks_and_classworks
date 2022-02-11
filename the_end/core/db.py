import sqlite3
from typing import Iterator
from contextlib import contextmanager


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect("data/db.sqlite3")
    yield conn
    conn.commit()
