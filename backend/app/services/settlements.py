import sqlite3

from app.domain.settlements import Settlement, calculate_settlements
from app.services.balances import get_group_balances


def get_group_settlements(
    connection: sqlite3.Connection,
    group_id: int,
) -> list[Settlement]:
    balances = get_group_balances(
        connection,
        group_id,
    )

    return calculate_settlements(balances)