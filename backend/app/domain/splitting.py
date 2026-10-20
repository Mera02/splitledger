def split_equally(amount_cents: int, member_ids: list[int]) -> dict[int, int]:
    if amount_cents <= 0:
        raise ValueError("Amount must be greater than zero.")

    if not member_ids:
        raise ValueError("At least one member is required.")

    if len(set(member_ids)) != len(member_ids):
        raise ValueError("Member IDs must be unique.")

    ordered_member_ids = sorted(member_ids)

    base_share, remainder = divmod(
        amount_cents,
        len(ordered_member_ids),
    )

    shares = {}

    for index, member_id in enumerate(ordered_member_ids):
        extra_cent = 1 if index < remainder else 0
        shares[member_id] = base_share + extra_cent

    return shares