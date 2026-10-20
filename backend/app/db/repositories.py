import sqlite3


def create_group(
    connection: sqlite3.Connection,
    name: str,
) -> int:
    cursor = connection.execute(
        """
        INSERT INTO groups (name)
        VALUES (?)
        """,
        (name,),
    )

    return cursor.lastrowid


def list_groups(
    connection: sqlite3.Connection,
) -> list[dict]:
    rows = connection.execute(
        """
        SELECT id, name, created_at
        FROM groups
        ORDER BY id
        """
    ).fetchall()

    return [dict(row) for row in rows]


def create_member(
    connection: sqlite3.Connection,
    group_id: int,
    name: str,
    normalized_name: str,
) -> int:
    cursor = connection.execute(
        """
        INSERT INTO members (
            group_id,
            name,
            normalized_name
        )
        VALUES (?, ?, ?)
        """,
        (
            group_id,
            name,
            normalized_name,
        ),
    )

    return cursor.lastrowid


def list_members(
    connection: sqlite3.Connection,
    group_id: int,
) -> list[dict]:
    rows = connection.execute(
        """
        SELECT id, group_id, name, created_at
        FROM members
        WHERE group_id = ?
        ORDER BY id
        """,
        (group_id,),
    ).fetchall()

    return [dict(row) for row in rows]


def create_expense(
    connection: sqlite3.Connection,
    group_id: int,
    payer_member_id: int,
    description: str,
    amount_cents: int,
) -> int:
    cursor = connection.execute(
        """
        INSERT INTO expenses (
            group_id,
            payer_member_id,
            description,
            amount_cents
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            group_id,
            payer_member_id,
            description,
            amount_cents,
        ),
    )

    return cursor.lastrowid


def create_expense_share(
    connection: sqlite3.Connection,
    expense_id: int,
    member_id: int,
    share_cents: int,
) -> None:
    connection.execute(
        """
        INSERT INTO expense_shares (
            expense_id,
            member_id,
            share_cents
        )
        VALUES (?, ?, ?)
        """,
        (
            expense_id,
            member_id,
            share_cents,
        ),
    )



def get_total_paid_by_member(
    connection: sqlite3.Connection,
    group_id: int,
) -> dict[int, int]:
    rows = connection.execute(
        """
        SELECT
            m.id AS member_id,
            COALESCE(SUM(e.amount_cents), 0) AS total_paid
        FROM members m
        LEFT JOIN expenses e
            ON e.payer_member_id = m.id
        WHERE m.group_id = ?
        GROUP BY m.id
        ORDER BY m.id
        """,
        (group_id,),
    ).fetchall()

    return {
        row["member_id"]: row["total_paid"]
        for row in rows
    }


def get_total_owed_by_member(
    connection: sqlite3.Connection,
    group_id: int,
) -> dict[int, int]:
    rows = connection.execute(
        """
        SELECT
            m.id AS member_id,
            COALESCE(SUM(es.share_cents), 0) AS total_owed
        FROM members m
        LEFT JOIN expense_shares es
            ON es.member_id = m.id
        WHERE m.group_id = ?
        GROUP BY m.id
        ORDER BY m.id
        """,
        (group_id,),
    ).fetchall()

    return {
        row["member_id"]: row["total_owed"]
        for row in rows
    }


def list_expenses(
    connection: sqlite3.Connection,
    group_id: int,
) -> list[dict]:
    rows = connection.execute(
        """
        SELECT
            e.id,
            e.group_id,
            e.payer_member_id,
            m.name AS payer_name,
            e.description,
            e.amount_cents,
            e.created_at
        FROM expenses AS e
        JOIN members AS m
            ON m.id = e.payer_member_id
        WHERE e.group_id = ?
        ORDER BY e.id DESC
        """,
        (group_id,),
    ).fetchall()

    return [dict(row) for row in rows]