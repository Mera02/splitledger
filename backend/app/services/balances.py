import sqlite3

from app.db.repositories import (
    get_total_owed_by_member,
    get_total_paid_by_member,
)
from app.domain.balances import calculate_balances


def get_group_balances(
    connection: sqlite3.Connection,
    group_id: int,
) -> dict[int, int]:
    total_paid = get_total_paid_by_member(
        connection,
        group_id,
    )

    total_owed = get_total_owed_by_member(
        connection,
        group_id,
    )

    return calculate_balances(
        total_paid,
        total_owed,
    )