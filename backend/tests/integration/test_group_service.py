import pytest

from app.db.connection import get_connection
from app.db.repositories import list_groups, list_members
from app.db.schema import initialize_database
from app.services.groups import create_group, add_member


def test_create_group_and_member(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)
    connection = get_connection(db_path)

    try:
        group_id = create_group(
            connection,
            "Mostar Trip",
        )

        member_id = add_member(
            connection,
            group_id,
            "Faris",
        )

        groups = list_groups(connection)
        members = list_members(connection, group_id)

        assert group_id == 1
        assert member_id == 1
        assert groups[0]["name"] == "Mostar Trip"
        assert members[0]["name"] == "Faris"

    finally:
        connection.close()


def test_reject_duplicate_member(tmp_path):
    db_path = tmp_path / "test.db"

    initialize_database(db_path)
    connection = get_connection(db_path)

    try:
        group_id = create_group(
            connection,
            "Mostar Trip",
        )

        add_member(
            connection,
            group_id,
            "Faris",
        )

        with pytest.raises(
            ValueError,
            match="Member already exists in this group."
        ):
            add_member(
                connection,
                group_id,
                " FARIS ",
            )

    finally:
        connection.close()