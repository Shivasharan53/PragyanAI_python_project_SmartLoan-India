SmartLoan India - EMI Calculator

Calculates:
1. Monthly EMI
2. Total interest payable
3. Total repayment

For educational and comparison purposes only.
"""


def calculate_emi(principal, annual_interest_rate, tenure_years):
    """
    Calculate loan EMI.

    Parameters
    ----------
    principal : float
        Loan amount in rupees.

    annual_interest_rate : float
        Annual interest rate in percent.

    tenure_years : int or float
        Loan tenure in years.

    Returns
    -------
    tuple
        (monthly_emi, total_interest, total_payment)
    """

    principal = float(principal)
    annual_interest_rate = float(annual_interest_rate)
    tenure_years = float(tenure_years)

    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if tenure_years <= 0:
        raise ValueError("Loan tenure must be greater than zero.")

    months = int(round(tenure_years * 12))

    if months <= 0:
        raise ValueError("Loan tenure must include at least one month.")

    monthly_rate = annual_interest_rate / (12 * 100)

    # Zero-interest loan
    if monthly_rate == 0:
        emi = principal / months
        total_payment = principal
        total_interest = 0.0

    else:
        # Standard reducing-balance EMI formula
        factor = (1 + monthly_rate) ** months

        emi = (
            principal
            * monthly_rate
            * factor
            / (factor - 1)
        )

        total_payment = emi * months
        total_interest = total_payment - principal

    # Avoid tiny negative values caused by floating-point rounding.
    total_interest = max(0.0, total_interest)

    return (
        round(emi, 2),
        round(total_interest, 2),
        round(total_payment, 2),
    )


# ==========================================================
# QUICK TEST
# ==========================================================

if __name__ == "__main__":
    amount = 500000
    rate = 10
    tenure = 5

    emi, interest, total = calculate_emi(
        amount,
        rate,
        tenure,
    )

    print(f"Loan Amount: ₹{amount:,.2f}")
    print(f"Annual Interest Rate: {rate}%")
    print(f"Tenure: {tenure} years")
    print(f"Monthly EMI: ₹{emi:,.2f}")
    print(f"Total Interest: ₹{interest:,.2f}")
    print(f"Total Repayment: ₹{total:,.2f}")
