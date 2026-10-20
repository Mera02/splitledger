import json

import typer

from app.db.connection import get_connection
from app.db.repositories import (
    list_expenses,
    list_groups,
    list_members,
)
from app.db.schema import initialize_database
from app.services.balances import get_group_balances
from app.services.expenses import create_expense
from app.services.groups import (
    add_member,
    create_group,
)
from app.services.settlements import get_group_settlements


app = typer.Typer(
    help="SplitLedger command-line interface."
)


def format_money(cents: int) -> str:
    return f"{cents / 100:.2f} KM"


def print_json(data: object) -> None:
    typer.echo(
        json.dumps(
            data,
            ensure_ascii=False,
        )
    )


@app.command("group-create")
def group_create(
    name: str,
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON.",
    ),
) -> None:
    initialize_database()
    connection = get_connection()

    try:
        group_id = create_group(
            connection,
            name,
        )

        if json_output:
            print_json(
                {
                    "id": group_id,
                    "name": name,
                }
            )
        else:
            typer.echo(
                f"Created group {group_id}: {name}"
            )

    except ValueError as error:
        if json_output:
            print_json(
                {
                    "error": str(error),
                }
            )
        else:
            typer.echo(
                f"Error: {error}",
                err=True,
            )

        raise typer.Exit(code=1)

    finally:
        connection.close()


@app.command("group-list")
def group_list(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON.",
    ),
) -> None:
    initialize_database()
    connection = get_connection()

    try:
        groups = list_groups(connection)

        if json_output:
            print_json(groups)
            return

        if not groups:
            typer.echo("No groups found.")
            return

        for group in groups:
            typer.echo(
                f'{group["id"]}: {group["name"]}'
            )

    finally:
        connection.close()


@app.command("member-add")
def member_add(
    group_id: int,
    name: str,
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON.",
    ),
) -> None:
    initialize_database()
    connection = get_connection()

    try:
        member_id = add_member(
            connection,
            group_id,
            name,
        )

        if json_output:
            print_json(
                {
                    "id": member_id,
                    "group_id": group_id,
                    "name": name,
                }
            )
        else:
            typer.echo(
                f"Added member {member_id}: {name}"
            )

    except ValueError as error:
        if json_output:
            print_json(
                {
                    "error": str(error),
                }
            )
        else:
            typer.echo(
                f"Error: {error}",
                err=True,
            )

        raise typer.Exit(code=1)

    finally:
        connection.close()


@app.command("member-list")
def member_list(
    group_id: int,
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON.",
    ),
) -> None:
    initialize_database()
    connection = get_connection()

    try:
        members = list_members(
            connection,
            group_id,
        )

        if json_output:
            print_json(members)
            return

        if not members:
            typer.echo("No members found.")
            return

        for member in members:
            typer.echo(
                f'{member["id"]}: {member["name"]}'
            )

    finally:
        connection.close()


@app.command("expense-add")
def expense_add(
    group_id: int,
    payer_member_id: int,
    description: str,
    amount: str,
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON.",
    ),
) -> None:
    initialize_database()
    connection = get_connection()

    try:
        expense_id = create_expense(
            connection,
            group_id,
            payer_member_id,
            description,
            amount,
        )

        if json_output:
            print_json(
                {
                    "id": expense_id,
                    "group_id": group_id,
                    "payer_member_id":
                        payer_member_id,
                    "description": description,
                    "amount": amount,
                }
            )
        else:
            typer.echo(
                f"Created expense {expense_id}: "
                f"{description} ({amount} KM)"
            )

    except ValueError as error:
        if json_output:
            print_json(
                {
                    "error": str(error),
                }
            )
        else:
            typer.echo(
                f"Error: {error}",
                err=True,
            )

        raise typer.Exit(code=1)

    finally:
        connection.close()


@app.command("expense-list")
def expense_list(
    group_id: int,
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON.",
    ),
) -> None:
    initialize_database()
    connection = get_connection()

    try:
        expenses = list_expenses(
            connection,
            group_id,
        )

        if json_output:
            print_json(expenses)
            return

        if not expenses:
            typer.echo("No expenses found.")
            return

        for expense in expenses:
            typer.echo(
                f'{expense["id"]}: '
                f'{expense["description"]} | '
                f'{format_money(expense["amount_cents"])} | '
                f'paid by {expense["payer_name"]}'
            )

    finally:
        connection.close()


@app.command("balances")
def balances(
    group_id: int,
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON.",
    ),
) -> None:
    initialize_database()
    connection = get_connection()

    try:
        members = list_members(
            connection,
            group_id,
        )

        group_balances = get_group_balances(
            connection,
            group_id,
        )

        result = [
            {
                "member_id": member["id"],
                "member_name": member["name"],
                "balance_cents":
                    group_balances.get(
                        member["id"],
                        0,
                    ),
            }
            for member in members
        ]

        if json_output:
            print_json(result)
            return

        if not result:
            typer.echo("No balances found.")
            return

        for balance in result:
            amount = balance["balance_cents"]

            sign = "+" if amount > 0 else ""

            typer.echo(
                f'{balance["member_name"]}: '
                f'{sign}{format_money(amount)}'
            )

    finally:
        connection.close()


@app.command("settlements")
def settlements(
    group_id: int,
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON.",
    ),
) -> None:
    initialize_database()
    connection = get_connection()

    try:
        members = list_members(
            connection,
            group_id,
        )

        member_names = {
            member["id"]: member["name"]
            for member in members
        }

        group_settlements = get_group_settlements(
            connection,
            group_id,
        )

        result = [
            {
                "from_member_id":
                    settlement.from_member_id,
                "from_member_name":
                    member_names[
                        settlement.from_member_id
                    ],
                "to_member_id":
                    settlement.to_member_id,
                "to_member_name":
                    member_names[
                        settlement.to_member_id
                    ],
                "amount_cents":
                    settlement.amount_cents,
            }
            for settlement in group_settlements
        ]

        if json_output:
            print_json(result)
            return

        if not result:
            typer.echo(
                "Everyone is settled up."
            )
            return

        for settlement in result:
            typer.echo(
                f'{settlement["from_member_name"]} '
                f'-> '
                f'{settlement["to_member_name"]}: '
                f'{format_money(settlement["amount_cents"])}'
            )

    finally:
        connection.close()


if __name__ == "__main__":
    app()