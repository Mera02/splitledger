def calculate_balances(
    total_paid: dict[int, int],
    total_owed: dict[int, int],
) -> dict[int, int]:
    member_ids = set(total_paid) | set(total_owed)

    if any(amount < 0 for amount in total_paid.values()):
        raise ValueError("Paid amounts cannot be negative.")

    if any(amount < 0 for amount in total_owed.values()):
        raise ValueError("Owed amounts cannot be negative.")

    if sum(total_paid.values()) != sum(total_owed.values()):
        raise ValueError("Total paid must equal total owed.")

    balances = {}

    for member_id in member_ids:
        paid = total_paid.get(member_id, 0)
        owed = total_owed.get(member_id, 0)

        balances[member_id] = paid - owed

    return balances