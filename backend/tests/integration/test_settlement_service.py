from app.db.connection import get_connection
from app.db.schema import initialize_database
from app.domain.settlements import Settlement
from app.services.expenses import create_expense
from app.services.groups import create_group, add_member
from app.services.settlements import get_group_settlements


def test_calculate_settlements_from_stored_expenses(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)
    connection = get_connection(db_path)

    try:
        group_id = create_group(
            connection,
            "Mostar Trip",
        )

        faris_id = add_member(
            connection,
            group_id,
            "Faris",
        )

        ada_id = add_member(
            connection,
            group_id,
            "Ada",
        )

        amar_id = add_member(
            connection,
            group_id,
            "Amar",
        )

        create_expense(
            connection,
            group_id,
            faris_id,
            "Apartment",
            "100.00",
        )

        create_expense(
            connection,
            group_id,
            ada_id,
            "Dinner",
            "30.00",
        )

        settlements = get_group_settlements(
            connection,
            group_id,
        )

        assert settlements == [
            Settlement(
                from_member_id=ada_id,
                to_member_id=faris_id,
                amount_cents=1333,
            ),
            Settlement(
                from_member_id=amar_id,
                to_member_id=faris_id,
                amount_cents=4333,
            ),
        ]

    finally:
        connection.close()