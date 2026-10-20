from dataclasses import dataclass


@dataclass(frozen=True)
class Settlement:
    from_member_id: int
    to_member_id: int
    amount_cents: int


def calculate_settlements(
    balances: dict[int, int],
) -> list[Settlement]:
    if sum(balances.values()) != 0:
        raise ValueError("Balances must sum to zero.")

    debtors = [
        [member_id, -balance]
        for member_id, balance in balances.items()
        if balance < 0
    ]

    creditors = [
        [member_id, balance]
        for member_id, balance in balances.items()
        if balance > 0
    ]

    debtors.sort(key=lambda item: item[0])
    creditors.sort(key=lambda item: item[0])

    settlements = []

    debtor_index = 0
    creditor_index = 0

    while (
        debtor_index < len(debtors)
        and creditor_index < len(creditors)
    ):
        debtor_id, debt = debtors[debtor_index]
        creditor_id, credit = creditors[creditor_index]

        amount = min(debt, credit)

        settlements.append(
            Settlement(
                from_member_id=debtor_id,
                to_member_id=creditor_id,
                amount_cents=amount,
            )
        )

        debtors[debtor_index][1] -= amount
        creditors[creditor_index][1] -= amount

        if debtors[debtor_index][1] == 0:
            debtor_index += 1

        if creditors[creditor_index][1] == 0:
            creditor_index += 1

    return settlements