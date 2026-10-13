
# ==========================================================
# SMARTLOAN INDIA - LOAN DATA
# ==========================================================
# Loan information is indicative. Verify current rates,
# eligibility and terms on the official bank websites.
# ==========================================================

BANKS = [
    "SBI",
    "HDFC Bank",
    "ICICI Bank",
    "Axis Bank",
    "Kotak Mahindra Bank",
    "Bank of Baroda",
    "Punjab National Bank",
    "Canara Bank",
    "Union Bank of India",
    "Indian Bank",
    "Bank of India",
    "Bank of Maharashtra",
    "IDFC FIRST Bank",
    "Federal Bank",
    "IndusInd Bank",
    "YES Bank",
]

BANK_WEBSITES = {
    "SBI": "https://sbi.bank.in/",
    "HDFC Bank": "https://www.hdfc.bank.in/",
    "ICICI Bank": "https://www.icici.bank.in/",
    "Axis Bank": "https://www.axisbank.com/",
    "Kotak Mahindra Bank": "https://www.kotak.bank.in/",
    "Bank of Baroda": "https://www.bankofbaroda.in/",
    "Punjab National Bank": "https://www.pnbindia.in/",
    "Canara Bank": "https://www.canarabank.com/",
    "Union Bank of India": "https://www.unionbankofindia.bank.in/",
    "Indian Bank": "https://www.indianbank.in/",
    "Bank of India": "https://bankofindia.co.in/",
    "Bank of Maharashtra": "https://bankofmaharashtra.in/",
    "IDFC FIRST Bank": "https://www.idfcfirstbank.com/",
    "Federal Bank": "https://www.federalbank.co.in/",
    "IndusInd Bank": "https://www.indusind.com/",
    "YES Bank": "https://www.yesbank.in/",
}

def product(
    available=True,
    min_amount=None,
    max_amount=None,
    interest_rate=None,
    rate_text=None,
    max_tenure=None,
    amount_text=None,
    eligibility_text=None,
    source="Verify with the official bank",
    source_url=None,
):
    return {
        "available": available,
        "min_amount": min_amount,
        "max_amount": max_amount,
        "interest_rate": interest_rate,
        "rate_text": rate_text,
        "max_tenure": max_tenure,
        "amount_text": amount_text,
        "eligibility_text": eligibility_text,
        "source": source,
        "source_url": source_url,
    }


# Loan categories supported by the application
LOAN_CATEGORIES = [
    "Personal Loan",
    "Education Loan",
    "Home Loan",
    "Car Loan",
    "Two-Wheeler Loan",
    "Gold Loan",
    "Business Loan",
    "Loan Against Property",
    "Agriculture Loan",
    "Consumer Durable Loan",
]

# General product information is not a confirmation that every
# bank offers every category. Verify product availability first.
LOAN_DATA = {}

for category in LOAN_CATEGORIES:
    LOAN_DATA[category] = {}

    for bank in BANKS:
        LOAN_DATA[category][bank] = product(
            available=True,
            amount_text="Check the bank's current scheme and eligibility",
            rate_text="Check the bank's current interest rate",
            eligibility_text=(
                "Eligibility, income, credit score and documentation "
                "depend on the bank and loan scheme."
            ),
            source_url=BANK_WEBSITES[bank],
        )


# Known indicative examples. Verify current terms with the bank.
LOAN_DATA["Personal Loan"]["SBI"].update(
    max_amount=3500000,
    amount_text="Up to ₹35 lakh; verify current eligibility",
)

LOAN_DATA["Personal Loan"]["HDFC Bank"].update(
    min_amount=25000,
    max_amount=4000000,
    amount_text="₹25,000–₹40 lakh; verify current eligibility",
    rate_text="Check current rate with HDFC Bank",
)

LOAN_DATA["Personal Loan"]["ICICI Bank"].update(
    min_amount=50000,
    max_amount=5000000,
    interest_rate=10.60,
    rate_text="Indicative example: 10.60% onwards; verify current rate",
    max_tenure=6,
    amount_text="₹50,000–₹50 lakh; verify current eligibility",
)

LOAN_DATA["Personal Loan"]["Axis Bank"].update(
    max_amount=4000000,
    amount_text="Up to ₹40 lakh; verify current eligibility",
)

LOAN_DATA["Education Loan"]["SBI"].update(
    amount_text=(
        "Scheme-dependent; amount and collateral requirements "
        "depend on the course and institution"
    ),
    source_url=(
        "https://sbi.bank.in/web/personal-banking/loans/education-loans"
    ),
)

LOAN_DATA["Education Loan"]["HDFC Bank"].update(
    max_amount=15000000,
    amount_text="Up to ₹1.5 crore; verify current eligibility",
)

LOAN_DATA["Education Loan"]["ICICI Bank"].update(
    amount_text=(
        "Loan amount depends on study destination, course "
        "and eligibility; check the official website"
    ),
)

LOAN_DATA["Home Loan"]["SBI"].update(
    max_tenure=30,
    amount_text="Depends on property value and eligibility",
)

LOAN_DATA["Home Loan"]["HDFC Bank"].update(
    max_tenure=30,
    amount_text="Depends on property value and eligibility",
)

LOAN_DATA["Home Loan"]["ICICI Bank"].update(
    max_amount=50000000,
    max_tenure=30,
    amount_text="Up to ₹5 crore; verify current eligibility",
)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_amount_text(product_data):
    if not isinstance(product_data, dict):
        return "Amount details unavailable"

    text = product_data.get("amount_text")
    if text:
        return text

    minimum = product_data.get("min_amount")
    maximum = product_data.get("max_amount")

    if minimum is not None and maximum is not None:
        return f"₹{minimum:,.0f} – ₹{maximum:,.0f}"
    if maximum is not None:
        return f"Up to ₹{maximum:,.0f}"
    if minimum is not None:
        return f"From ₹{minimum:,.0f}"

    return "Depends on bank policy and eligibility"


def get_rate_text(product_data):
    if not isinstance(product_data, dict):
        return "Rate unavailable"

    text = product_data.get("rate_text")
    if text:
        return text

    rate = product_data.get("interest_rate")
    if rate is not None:
        return f"{float(rate):.2f}% per annum"

    return "Check the official bank website"


def get_tenure_text(product_data):
    if not isinstance(product_data, dict):
        return "Tenure unavailable"

    tenure = product_data.get("max_tenure")
    if tenure is not None:
        return f"Up to {float(tenure):g} years"

    return "Depends on the loan scheme"


def get_loan_product(category, bank):
    return LOAN_DATA.get(category, {}).get(bank)


def get_available_banks(category):
    category_data = LOAN_DATA.get(category, {})
    return [
        bank
        for bank, details in category_data.items()
        if details.get("available", False)
    ]


def get_loan_categories():
    return list(LOAN_DATA.keys())
