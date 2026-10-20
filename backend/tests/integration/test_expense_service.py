from app.db.connection import get_connection
from app.db.schema import initialize_database
from app.services.expenses import create_expense
from app.services.groups import create_group, add_member


def test_create_equal_split_expense(tmp_path):
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

        add_member(
            connection,
            group_id,
            "Ada",
        )

        add_member(
            connection,
            group_id,
            "Amar",
        )

        expense_id = create_expense(
            connection=connection,
            group_id=group_id,
            payer_member_id=faris_id,
            description="Apartment",
            amount="100.00",
        )

        expense = connection.execute(
            """
            SELECT amount_cents
            FROM expenses
            WHERE id = ?
            """,
            (expense_id,),
        ).fetchone()

        shares = connection.execute(
            """
            SELECT member_id, share_cents
            FROM expense_shares
            WHERE expense_id = ?
            ORDER BY member_id
            """,
            (expense_id,),
        ).fetchall()

        assert expense["amount_cents"] == 10000

        assert [
            row["share_cents"]
            for row in shares
        ] == [
            3334,
            3333,
            3333,
        ]

    finally:
        connection.close()