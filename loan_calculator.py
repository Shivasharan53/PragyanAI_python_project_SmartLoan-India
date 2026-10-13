EMI calculation helpers for SmartLoan India.


def calculate_emi(principal, annual_interest_rate, tenure_years):
    """
    Calculate monthly EMI, total interest, and total repayment.

    Returns:
        tuple: (monthly_emi, total_interest, total_payment)
    """
    principal = float(principal)
    annual_interest_rate = float(annual_interest_rate)
    tenure_years = float(tenure_years)

    if principal < 0:
        raise ValueError("Loan amount cannot be negative.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if tenure_years <= 0:
        raise ValueError("Loan tenure must be greater than zero.")

    months = round(tenure_years * 12)

    if months <= 0:
        raise ValueError("Loan tenure must be at least one month.")

    if principal == 0:
        return 0.0, 0.0, 0.0

    monthly_rate = annual_interest_rate / 1200

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


if __name__ == "__main__":
    amount = 500000
    rate = 10
    tenure = 5

    emi, interest, total = calculate_emi(amount, rate, tenure)

    print(f"Loan Amount: ₹{amount:,.2f}")
    print(f"Interest Rate: {rate}% per annum")
    print(f"Tenure: {tenure} years")
    print(f"Monthly EMI: ₹{emi:,.2f}")
    print(f"Total Interest: ₹{interest:,.2f}")
    print(f"Total Repayment: ₹{total:,.2f}")
