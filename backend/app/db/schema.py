from pathlib import Path

from app.db.connection import get_connection


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,

    UNIQUE (group_id, normalized_name)
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL,
    payer_member_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,

    FOREIGN KEY (payer_member_id)
        REFERENCES members(id)
);

CREATE TABLE IF NOT EXISTS expense_shares (
    expense_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    share_cents INTEGER NOT NULL CHECK (share_cents >= 0),

    PRIMARY KEY (expense_id, member_id),

    FOREIGN KEY (expense_id)
        REFERENCES expenses(id)
        ON DELETE CASCADE,

    FOREIGN KEY (member_id)
        REFERENCES members(id)
);
"""


def initialize_database(
    db_path: str | Path | None = None,
) -> None:
    connection = get_connection(db_path)

    try:
        connection.executescript(SCHEMA_SQL)
        connection.commit()
    finally:
        connection.close()