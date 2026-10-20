import sqlite3

from app.db.repositories import (
    create_expense as insert_expense,
    create_expense_share,
    list_members,
)
from app.domain.money import parse_amount_to_cents
from app.domain.splitting import split_equally


def create_expense(
    connection: sqlite3.Connection,
    group_id: int,
    payer_member_id: int,
    description: str,
    amount: str,
) -> int:
    cleaned_description = " ".join(
        description.strip().split()
    )

    if not cleaned_description:
        raise ValueError("Expense description is required.")

    members = list_members(connection, group_id)

    if not members:
        raise ValueError(
            "Group must have at least one member."
        )

    member_ids = [
        member["id"]
        for member in members
    ]

    if payer_member_id not in member_ids:
        raise ValueError(
            "Payer must belong to the group."
        )

    amount_cents = parse_amount_to_cents(amount)

    shares = split_equally(
        amount_cents,
        member_ids,
    )

    try:
        expense_id = insert_expense(
            connection,
            group_id,
            payer_member_id,
            cleaned_description,
            amount_cents,
        )

        for member_id, share_cents in shares.items():
            create_expense_share(
                connection,
                expense_id,
                member_id,
                share_cents,
            )

        connection.commit()

        return expense_id

    except Exception:
        connection.rollback()
        raise