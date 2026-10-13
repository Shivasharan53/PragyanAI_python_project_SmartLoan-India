
def calculate_emi(principal, annual_rate, years):
    """Calculate monthly EMI, total interest and total repayment."""

    principal = float(principal)
    annual_rate = float(annual_rate)
    years = float(years)

    if principal < 0:
        raise ValueError("Loan amount cannot be negative.")
    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")
    if years <= 0:
        raise ValueError("Loan tenure must be greater than zero.")

    months = int(years * 12)

    if months <= 0:
        raise ValueError("Loan tenure must be at least one month.")

    if principal == 0:
        return 0.0, 0.0, 0.0

    monthly_rate = annual_rate / 1200

    if monthly_rate == 0:
        emi = principal / months
    else:
        factor = (1 + monthly_rate) ** months
        emi = principal * monthly_rate * factor / (factor - 1)

    total_payment = emi * months
    total_interest = max(0.0, total_payment - principal)

    return (
        round(emi, 2),
        round(total_interest, 2),
        round(total_payment, 2),
    )
