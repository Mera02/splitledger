import os
import sqlite3
from pathlib import Path


DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "splitledger.db"


def get_connection(
    db_path: str | Path | None = None,
) -> sqlite3.Connection:
    path = Path(
        db_path
        or os.getenv("SPLITLEDGER_DB_PATH")
        or DEFAULT_DB_PATH
    )

    connection = sqlite3.connect(path)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection