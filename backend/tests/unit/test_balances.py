import pytest

from app.domain.balances import calculate_balances


def test_calculate_balances():
    result = calculate_balances(
        total_paid={
            1: 10000,
        },
        total_owed={
            1: 3334,
            2: 3333,
            3: 3333,
        },
    )

    assert result == {
        1: 6666,
        2: -3333,
        3: -3333,
    }


def test_balances_sum_to_zero():
    result = calculate_balances(
        total_paid={
            1: 10000,
        },
        total_owed={
            1: 3334,
            2: 3333,
            3: 3333,
        },
    )

    assert sum(result.values()) == 0


def test_reject_mismatched_paid_and_owed_totals():
    with pytest.raises(
        ValueError,
        match="Total paid must equal total owed."
    ):
        calculate_balances(
            total_paid={1: 10000},
            total_owed={
                1: 3333,
                2: 3333,
                3: 3333,
            },
        )


def test_reject_negative_paid_amount():
    with pytest.raises(
        ValueError,
        match="Paid amounts cannot be negative."
    ):
        calculate_balances(
            total_paid={1: -100},
            total_owed={1: -100},
        )