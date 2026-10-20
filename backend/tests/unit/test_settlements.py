import pytest

from app.domain.settlements import (
    Settlement,
    calculate_settlements,
)


def test_calculate_simple_settlements():
    result = calculate_settlements(
        {
            1: 6666,
            2: -3333,
            3: -3333,
        }
    )

    assert result == [
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


def test_calculate_settlements_with_multiple_creditors():
    result = calculate_settlements(
        {
            1: 5000,
            2: 2000,
            3: -3000,
            4: -4000,
        }
    )

    assert result == [
        Settlement(3, 1, 3000),
        Settlement(4, 1, 2000),
        Settlement(4, 2, 2000),
    ]


def test_no_settlements_when_everyone_is_balanced():
    result = calculate_settlements(
        {
            1: 0,
            2: 0,
            3: 0,
        }
    )

    assert result == []


def test_reject_balances_that_do_not_sum_to_zero():
    with pytest.raises(
        ValueError,
        match="Balances must sum to zero."
    ):
        calculate_settlements(
            {
                1: 5000,
                2: -4000,
            }
        )


def test_settlement_amounts_are_always_positive():
    result = calculate_settlements(
        {
            1: 7000,
            2: -3000,
            3: -4000,
        }
    )

    assert all(
        settlement.amount_cents > 0
        for settlement in result
    )