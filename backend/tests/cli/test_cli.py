import json

from typer.testing import CliRunner

from app.cli import app


runner = CliRunner()


def test_complete_cli_flow(tmp_path, monkeypatch):
    db_path = tmp_path / "cli-test.db"

    monkeypatch.setenv(
        "SPLITLEDGER_DB_PATH",
        str(db_path),
    )

    group_result = runner.invoke(
        app,
        [
            "group-create",
            "CLI Test",
            "--json",
        ],
    )

    assert group_result.exit_code == 0

    group = json.loads(group_result.stdout)
    group_id = group["id"]

    faris_result = runner.invoke(
        app,
        [
            "member-add",
            str(group_id),
            "Faris",
            "--json",
        ],
    )

    assert faris_result.exit_code == 0

    faris = json.loads(faris_result.stdout)

    ada_result = runner.invoke(
        app,
        [
            "member-add",
            str(group_id),
            "Ada",
            "--json",
        ],
    )

    assert ada_result.exit_code == 0

    ada = json.loads(ada_result.stdout)

    expense_result = runner.invoke(
        app,
        [
            "expense-add",
            str(group_id),
            str(faris["id"]),
            "Apartment",
            "90.00",
            "--json",
        ],
    )

    assert expense_result.exit_code == 0

    balances_result = runner.invoke(
        app,
        [
            "balances",
            str(group_id),
            "--json",
        ],
    )

    assert balances_result.exit_code == 0

    balances = json.loads(
        balances_result.stdout,
    )

    balances_by_name = {
        item["member_name"]:
            item["balance_cents"]
        for item in balances
    }

    assert balances_by_name == {
        "Faris": 4500,
        "Ada": -4500,
    }

    settlements_result = runner.invoke(
        app,
        [
            "settlements",
            str(group_id),
            "--json",
        ],
    )

    assert settlements_result.exit_code == 0

    settlements = json.loads(
        settlements_result.stdout,
    )

    assert settlements == [
        {
            "from_member_id":
                ada_result
                and json.loads(
                    ada_result.stdout,
                )["id"],
            "from_member_name": "Ada",
            "to_member_id": faris["id"],
            "to_member_name": "Faris",
            "amount_cents": 4500,
        }
    ]


def test_cli_rejects_negative_expense(
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "cli-error-test.db"

    monkeypatch.setenv(
        "SPLITLEDGER_DB_PATH",
        str(db_path),
    )

    group_result = runner.invoke(
        app,
        [
            "group-create",
            "Invalid Test",
            "--json",
        ],
    )

    group = json.loads(group_result.stdout)

    member_result = runner.invoke(
        app,
        [
            "member-add",
            str(group["id"]),
            "Faris",
            "--json",
        ],
    )

    member = json.loads(member_result.stdout)

    result = runner.invoke(
        app,
        [
            "expense-add",
            str(group["id"]),
            str(member["id"]),
            "Invalid expense",
            "--json",
            "--",
            "-10.00",
        ],
    )

    assert result.exit_code == 1

    error = json.loads(result.stdout)

    assert error == {
        "error":
            "Amount must be greater than zero."
    }