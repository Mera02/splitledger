from app.db.connection import get_connection
from app.db.repositories import (
    create_group,
    list_groups,
)
from app.db.schema import initialize_database


def test_create_and_list_group(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)

    connection = get_connection(db_path)

    try:
        group_id = create_group(
            connection,
            "Mostar Trip",
        )

        connection.commit()

        groups = list_groups(connection)

        assert group_id == 1

        assert len(groups) == 1

        assert groups[0]["id"] == 1
        assert groups[0]["name"] == "Mostar Trip"

    finally:
        connection.close()