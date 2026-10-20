import pytest

from app.domain.money import parse_amount_to_cents


def test_parse_valid_amount_to_cents():
    result = parse_amount_to_cents("100.00")

    assert result == 10000


def test_parse_minimum_valid_amount():
    result = parse_amount_to_cents("0.01")

    assert result == 1


def test_reject_amount_with_more_than_two_decimal_places():
    with pytest.raises(
        ValueError,
        match="Amount cannot have more than two decimal places."
    ):
        parse_amount_to_cents("12.345")


def test_reject_non_numeric_amount():
    with pytest.raises(
        ValueError,
        match="Amount must be a valid number."
    ):
        parse_amount_to_cents("abc")


def test_reject_zero_amount():
    with pytest.raises(
        ValueError,
        match="Amount must be greater than zero."
    ):
        parse_amount_to_cents("0")


def test_reject_negative_amount():
    with pytest.raises(
        ValueError,
        match="Amount must be greater than zero."
    ):
        parse_amount_to_cents("-10.00")


def test_accept_maximum_amount():
    result = parse_amount_to_cents("10000000.00")

    assert result == 1_000_000_000


def test_reject_amount_above_maximum():
    with pytest.raises(
        ValueError,
        match="Amount exceeds the maximum allowed value."
    ):
        parse_amount_to_cents("10000000.01")


def test_reject_empty_amount():
    with pytest.raises(
        ValueError,
        match="Amount is required."
    ):
        parse_amount_to_cents("   ")


def test_reject_nan():
    with pytest.raises(
        ValueError,
        match="Amount must be a finite number."
    ):
        parse_amount_to_cents("NaN")


def test_reject_infinity():
    with pytest.raises(
        ValueError,
        match="Amount must be a finite number."
    ):
        parse_amount_to_cents("Infinity")