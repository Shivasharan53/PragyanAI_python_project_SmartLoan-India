def calculate_emi(principal, annual_rate, years):
    if principal <= 0 or years <= 0 or annual_rate < 0:
        raise ValueError(
            "Principal and tenure must be positive; rate cannot be negative."
        )

    months = int(years * 12)
    monthly_rate = annual_rate / 1200

    if monthly_rate == 0:
        return principal / months

    factor = (1 + monthly_rate) ** months
    return principal * monthly_rate * factor / (factor - 1)


def calculate_loan_summary(principal, annual_rate, years):
    emi = calculate_emi(principal, annual_rate, years)
    total_payment = emi * int(years * 12)

    return {
        "monthly_emi": emi,
        "total_payment": total_payment,
        "total_interest": total_payment - principal,
    }
