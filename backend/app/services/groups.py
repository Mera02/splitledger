import sqlite3

from app.db.repositories import (
    create_group as insert_group,
    create_member as insert_member,
)


def clean_name(name: str) -> str:
    return " ".join(name.strip().split())


def create_group(
    connection: sqlite3.Connection,
    name: str,
) -> int:
    cleaned_name = clean_name(name)

    if not cleaned_name:
        raise ValueError("Group name is required.")

    if len(cleaned_name) > 80:
        raise ValueError("Group name is too long.")

    group_id = insert_group(connection, cleaned_name)
    connection.commit()

    return group_id


def add_member(
    connection: sqlite3.Connection,
    group_id: int,
    name: str,
) -> int:
    cleaned_name = clean_name(name)

    if not cleaned_name:
        raise ValueError("Member name is required.")

    if len(cleaned_name) > 80:
        raise ValueError("Member name is too long.")

    normalized_name = cleaned_name.casefold()

    try:
        member_id = insert_member(
            connection,
            group_id,
            cleaned_name,
            normalized_name,
        )

        connection.commit()

        return member_id

    except sqlite3.IntegrityError as error:
        connection.rollback()

        if "UNIQUE constraint failed" in str(error):
            raise ValueError(
                "Member already exists in this group."
            ) from None

        if "FOREIGN KEY constraint failed" in str(error):
            raise ValueError(
                "Group does not exist."
            ) from None

        raise