
# ==========================================================
# HELPER FUNCTIONS FOR SMARTLOAN INDIA
# ==========================================================

def get_amount_text(product_data):
    """Return the available loan amount as readable text."""
    if not isinstance(product_data, dict):
        return "Amount details unavailable"

    amount_text = product_data.get("amount_text")
    if amount_text:
        return amount_text

    min_amount = product_data.get("min_amount")
    max_amount = product_data.get("max_amount")

    if min_amount is not None and max_amount is not None:
        return f"₹{min_amount:,.0f} – ₹{max_amount:,.0f}"

    if max_amount is not None:
        return f"Up to ₹{max_amount:,.0f}"

    if min_amount is not None:
        return f"From ₹{min_amount:,.0f}"

    return "Depends on bank policy and eligibility"


def get_rate_text(product_data):
    """Return the interest rate as readable text."""
    if not isinstance(product_data, dict):
        return "Rate unavailable"

    rate_text = product_data.get("rate_text")
    if rate_text:
        return rate_text

    interest_rate = product_data.get("interest_rate")
    if interest_rate is not None:
        return f"{interest_rate:.2f}% per annum"

    return "Check the official bank website"


def get_tenure_text(product_data):
    """Return the maximum loan tenure as readable text."""
    if not isinstance(product_data, dict):
        return "Tenure unavailable"

    max_tenure = product_data.get("max_tenure")

    if max_tenure is not None:
        years = float(max_tenure)
        return f"Up to {years:g} years"

    return "Depends on the loan scheme"


def get_loan_product(category, bank):
    """Safely retrieve a loan product for a category and bank."""
    category_data = LOAN_DATA.get(category, {})
    product_data = category_data.get(bank)

    if not product_data:
        return None

    return product_data


def get_available_banks(category):
    """Return banks listed for a particular loan category."""
    category_data = LOAN_DATA.get(category, {})

    return [
        bank
        for bank, details in category_data.items()
        if details.get("available", True)
    ]


def get_loan_categories():
    """Return all available loan categories."""
    return list(LOAN_DATA.keys())
