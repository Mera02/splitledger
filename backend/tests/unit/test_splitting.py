import pytest

from app.domain.splitting import split_equally


def test_split_evenly_without_remainder():
    result = split_equally(9000, [1, 2, 3])

    assert result == {
        1: 3000,
        2: 3000,
        3: 3000,
    }


def test_split_with_one_remainder_cent():
    result = split_equally(10000, [1, 2, 3])

    assert result == {
        1: 3334,
        2: 3333,
        3: 3333,
    }


def test_remainder_is_assigned_by_ascending_member_id():
    result = split_equally(10000, [3, 1, 2])

    assert result == {
        1: 3334,
        2: 3333,
        3: 3333,
    }


def test_split_one_cent_between_three_members():
    result = split_equally(1, [1, 2, 3])

    assert result == {
        1: 1,
        2: 0,
        3: 0,
    }


def test_reject_empty_member_list():
    with pytest.raises(
        ValueError,
        match="At least one member is required."
    ):
        split_equally(10000, [])


def test_reject_duplicate_member_ids():
    with pytest.raises(
        ValueError,
        match="Member IDs must be unique."
    ):
        split_equally(10000, [1, 2, 2])



@pytest.mark.parametrize(
    ("amount_cents", "member_ids"),
    [
        (1, [1]),
        (1, [1, 2, 3]),
        (100, [1, 2, 3]),
        (10000, [1, 2, 3]),
        (99999, [4, 2, 8, 1]),
    ],
)
def test_split_never_creates_or_loses_money(amount_cents, member_ids):
    result = split_equally(amount_cents, member_ids)

    assert sum(result.values()) == amount_cents
