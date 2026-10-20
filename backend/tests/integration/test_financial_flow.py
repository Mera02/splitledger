from app.domain.balances import calculate_balances
from app.domain.money import parse_amount_to_cents
from app.domain.settlements import Settlement, calculate_settlements
from app.domain.splitting import split_equally


def test_complete_equal_expense_flow():
    amount_cents = parse_amount_to_cents("100.00")

    shares = split_equally(
        amount_cents=amount_cents,
        member_ids=[1, 2, 3],
    )

    balances = calculate_balances(
        total_paid={
            1: amount_cents,
        },
        total_owed=shares,
    )

    settlements = calculate_settlements(balances)

    assert amount_cents == 10000

    assert shares == {
        1: 3334,
        2: 3333,
        3: 3333,
    }

    assert balances == {
        1: 6666,
        2: -3333,
        3: -3333,
    }

    assert settlements == [
        Settlement(
            from_member_id=2,
            to_member_id=1,
            amount_cents=3333,
        ),
        Settlement(
            from_member_id=3,
            to_member_id=1,
            amount_cents=3333,
        ),
    ]