from decimal import Decimal, InvalidOperation


MAX_AMOUNT_CENTS = 1_000_000_000


def parse_amount_to_cents(amount: str) -> int:
    value = amount.strip()

    if not value:
        raise ValueError("Amount is required.")

    try:
        decimal_amount = Decimal(value)
    except InvalidOperation:
        raise ValueError("Amount must be a valid number.") from None

    if not decimal_amount.is_finite():
        raise ValueError("Amount must be a finite number.")

    if decimal_amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if decimal_amount.as_tuple().exponent < -2:
        raise ValueError("Amount cannot have more than two decimal places.")

    cents = int(decimal_amount * 100)

    if cents > MAX_AMOUNT_CENTS:
        raise ValueError("Amount exceeds the maximum allowed value.")

    return cents