from app.db.connection import get_connection
from app.db.schema import initialize_database
from app.services.balances import get_group_balances
from app.services.expenses import create_expense
from app.services.groups import create_group, add_member


def test_calculate_balances_from_stored_expenses(tmp_path):
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

        balances = get_group_balances(
            connection,
            group_id,
        )

        assert balances == {
            faris_id: 5666,
            ada_id: -1333,
            amar_id: -4333,
        }

        assert sum(balances.values()) == 0

    finally:
        connection.close()