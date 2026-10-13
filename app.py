
import streamlit as st
import pandas as pd

from loan_data import BANKS, BANK_WEBSITES, LOAN_DATA
from loan_calculator import calculate_emi


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="SmartLoan India",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# CUSTOM DESIGN
# ==========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f5f7fb;
        color: #111827;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }

    p, label, .stMarkdown, .stCaption {
        color: #374151;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg, #030712, #0f172a
        );
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    .hero {
        padding: 45px;
        border-radius: 24px;
        background: linear-gradient(
            135deg, #020617, #0f172a, #172554
        );
        margin-bottom: 28px;
        box-shadow: 0 15px 40px rgba(15,23,42,.15);
    }

    .hero-title {
        color: white;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero-text {
        color: #cbd5e1;
        font-size: 17px;
        line-height: 1.7;
    }

    .loan-card {
        min-height: 175px;
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(
            145deg, #111827, #0b1120
        );
        border: 1px solid #263244;
        margin-bottom: 12px;
        transition: .2s ease;
    }

    .loan-card:hover {
        border-color: #3b82f6;
        transform: translateY(-3px);
    }

    .loan-icon {
        font-size: 32px;
        margin-bottom: 12px;
    }

    .loan-title {
        color: white;
        font-size: 19px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .loan-description {
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.6;
    }

    [data-testid="stMetric"] {
        background: white;
        padding: 16px;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #475569 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
    }

    .footer {
        text-align: center;
        padding: 30px 10px;
        margin-top: 35px;
        border-top: 1px solid #e2e8f0;
        color: #64748b;
    }

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 650;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def format_amount(amount):
    if amount is None:
        return "Not specified"
    return f"₹{amount:,.0f}"


def get_amount_text(product):
    if not product:
        return "Not verified"

    text = product.get("amount_text")
    if text:
        return text

    minimum = product.get("min_amount")
    maximum = product.get("max_amount")

    if minimum is not None and maximum is not None:
        return f"₹{minimum:,.0f} – ₹{maximum:,.0f}"

    if maximum is not None:
        return f"Up to ₹{maximum:,.0f}"

    if minimum is not None:
        return f"From ₹{minimum:,.0f}"

    return "Depends on eligibility"


def get_rate_text(product):
    if not product:
        return "Not verified"

    text = product.get("rate_text")
    if text:
        return text

    rate = product.get("interest_rate")
    if rate is not None:
        return f"{rate}%"

    return "Check with bank"


def get_tenure_text(product):
    if not product:
        return "Not specified"

    tenure = product.get("max_tenure")
    if tenure is not None:
        return f"Up to {tenure} years"

    return "Depends on product"


def safe_emi(amount, rate, years):
    """Return EMI, total interest and total repayment."""
    return calculate_emi(
        float(amount),
        float(rate),
        int(years),
    )


def add_comparison(item):
    """Save or update a bank and loan combination."""
    saved = st.session_state.comparison_items

    for index, old_item in enumerate(saved):
        if (
            old_item["bank"] == item["bank"]
            and old_item["loan_type"] == item["loan_type"]
        ):
            saved[index] = item
            st.session_state.comparison_items = saved
            return

    saved.append(item)
    st.session_state.comparison_items = saved


def navigate_to_loan(loan_name):
    st.session_state.selected_loan = loan_name
    st.session_state.navigation = "🔍 Find Loan"
    st.session_state.find_loan_type = loan_name


def show_emi_results(amount, rate, years):
    emi, interest, total = safe_emi(amount, rate, years)

    c1, c2, c3 = st.columns(3)

    c1.metric("Monthly EMI", f"₹{emi:,.2f}")
    c2.metric("Total Interest", f"₹{interest:,.2f}")
    c3.metric("Total Repayment", f"₹{total:,.2f}")


# ==========================================================
# SESSION STATE
# ==========================================================

if "comparison_items" not in st.session_state:
    st.session_state.comparison_items = []

if "selected_loan" not in st.session_state:
    st.session_state.selected_loan = None

if "selected_bank" not in st.session_state:
    st.session_state.selected_bank = None

if "navigation" not in st.session_state:
    st.session_state.navigation = "🏠 Home"


# ==========================================================
# SIDEBAR NAVIGATION
# ==========================================================

with st.sidebar:
    st.markdown("## 🏦 SmartLoan India")
    st.caption("Smart • Simple • Transparent")
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Home",
            "🔍 Find Loan",
            "📊 Compare Loans",
            "🧮 EMI Calculator",
        ],
        key="navigation",
    )

    st.markdown("---")

    st.info(
        "Explore loan options, compare banks and "
        "calculate estimated monthly repayments."
    )

    st.caption(
        f"Saved comparisons: "
        f"{len(st.session_state.comparison_items)}"
    )


# ==========================================================
# HOME PAGE
# ==========================================================

if page == "🏠 Home":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">🏦 SmartLoan India</div>
            <div class="hero-text">
                Find, compare and calculate loans from major
                Indian banks — all in one place.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Choose the loan you need")

    st.write(
        "Select a category below to explore the available options."
    )

    loan_cards = [
        (
            "👤",
            "Personal Loan",
            "Flexible financing for personal and emergency needs.",
        ),
        (
            "🎓",
            "Education Loan",
            "Explore funding options for higher education.",
        ),
        (
            "🏠",
            "Home Loan",
            "Explore financing for purchasing or constructing a home.",
        ),
        (
            "🚗",
            "Car Loan",
            "Estimate financing for a new or used car.",
        ),
        (
            "🛵",
            "Two-Wheeler Loan",
            "Estimate financing for a bike or scooter.",
        ),
        (
            "🥇",
            "Gold Loan",
            "Explore borrowing options against eligible gold.",
        ),
        (
            "💼",
            "Business Loan",
            "Explore financing for business needs.",
        ),
        (
            "🏢",
            "Loan Against Property",
            "Explore loans secured against eligible property.",
        ),
        (
            "🚜",
            "Agriculture Loan",
            "Explore financing options for farming needs.",
        ),
    ]

    for start in range(0, len(loan_cards), 3):
        columns = st.columns(3)

        for col, card in zip(
            columns,
            loan_cards[start:start + 3],
        ):
            icon, title, description = card

            with col:
                st.markdown(
                    f"""
                    <div class="loan-card">
                        <div class="loan-icon">{icon}</div>
                        <div class="loan-title">{title}</div>
                        <div class="loan-description">
                            {description}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.button(
                    f"Explore {title}",
                    key=f"home_{title}",
                    use_container_width=True,
                    on_click=navigate_to_loan,
                    args=(title,),
                )

    st.markdown("---")
    st.subheader("How SmartLoan India works")

    a, b, c, d = st.columns(4)

    a.info("**1. Select loan**\n\nChoose a loan category.")
    b.info("**2. Select bank**\n\nExplore available bank data.")
    c.info("**3. Enter details**\n\nSet amount, rate and tenure.")
    d.info("**4. Compare EMI**\n\nReview estimated repayments.")

    st.warning(
        "Loan rates, fees, eligibility and limits can change. "
        "Verify current terms directly with the bank before applying."
    )


# ==========================================================
# FIND LOAN PAGE
# ==========================================================

elif page == "🔍 Find Loan":

    st.title("🔍 Find Your Loan")

    st.write(
        "Select a loan category and bank, then enter your "
        "requirements to estimate the repayment."
    )

    loan_types = list(LOAN_DATA.keys())

    if not loan_types:
        st.error("No loan categories are configured in loan_data.py.")
        st.stop()

    default_loan = st.session_state.selected_loan

    if default_loan not in loan_types:
        default_loan = loan_types[0]

    loan_type = st.selectbox(
        "🏦 Select Loan Type",
        loan_types,
        index=loan_types.index(default_loan),
        key="find_loan_type",
    )

    bank = st.selectbox(
        "🏛️ Select Bank",
        BANKS,
        key="find_bank",
    )

    st.session_state.selected_loan = loan_type
    st.session_state.selected_bank = bank

    product = LOAN_DATA.get(loan_type, {}).get(bank)

    st.markdown("---")

    if product is None:
        st.warning(
            f"No specific {loan_type} information is configured "
            f"for {bank} in this app."
        )

        st.info(
            "You can visit the bank's official website to "
            "check available products and eligibility."
        )

        if bank in BANK_WEBSITES:
            st.link_button(
                "🌐 Open Official Bank Website",
                BANK_WEBSITES[bank],
            )

    else:
        st.subheader(f"{bank} — {loan_type}")

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Minimum Loan",
            format_amount(product.get("min_amount")),
        )

        m2.metric(
            "Maximum Loan",
            format_amount(product.get("max_amount")),
        )

        m3.metric(
            "Interest Rate",
            get_rate_text(product),
        )

        st.caption(
            "Displayed figures may be indicative. Confirm current "
            "rates, charges and eligibility with the bank."
        )

        st.markdown("---")
        st.subheader("💰 Loan Requirements")

        valid_inputs = True

        # ----------------------------------------------
        # VEHICLE LOANS
        # ----------------------------------------------

        if loan_type in ("Car Loan", "Two-Wheeler Loan"):

            if loan_type == "Car Loan":
                vehicle_label = "🚗 On-Road Car Price (₹)"
                default_price = 1000000
                price_step = 10000
            else:
                vehicle_label = "🛵 On-Road Bike/Scooter Price (₹)"
                default_price = 120000
                price_step = 5000

            vehicle_price = st.number_input(
                vehicle_label,
                min_value=1000,
                value=default_price,
                step=price_step,
                key=f"{loan_type}_price",
            )

            down_payment = st.number_input(
                "💰 Down Payment (₹)",
                min_value=0,
                value=min(20000, vehicle_price),
                step=5000,
                key=f"{loan_type}_down",
            )

            if down_payment > vehicle_price:
                st.error("Down payment cannot exceed vehicle price.")
                valid_inputs = False

            loan_amount = max(0, vehicle_price - down_payment)

            st.info(f"Required Loan Amount: ₹{loan_amount:,.0f}")

        # ----------------------------------------------
        # HOME LOAN
        # ----------------------------------------------

        elif loan_type == "Home Loan":

            property_value = st.number_input(
                "🏠 Property Value (₹)",
                min_value=100000,
                value=5000000,
                step=100000,
            )

            down_payment = st.number_input(
                "💰 Down Payment (₹)",
                min_value=0,
                value=1000000,
                step=100000,
            )

            if down_payment > property_value:
                st.error("Down payment cannot exceed property value.")
                valid_inputs = False

            loan_amount = max(0, property_value - down_payment)

            st.info(f"Required Home Loan: ₹{loan_amount:,.0f}")

        # ----------------------------------------------
        # EDUCATION LOAN
        # ----------------------------------------------

        elif loan_type == "Education Loan":

            course_fee = st.number_input(
                "🎓 Total Course Fee (₹)",
                min_value=10000,
                value=800000,
                step=10000,
            )

            study_location = st.selectbox(
                "Study Location",
                ["India", "Abroad"],
            )

            loan_amount = st.number_input(
                "Required Education Loan (₹)",
                min_value=10000,
                value=min(500000, course_fee),
                step=10000,
            )

            if loan_amount > course_fee:
                st.error("Loan amount cannot exceed the course fee.")
                valid_inputs = False

        # ----------------------------------------------
        # GOLD LOAN
        # ----------------------------------------------

        elif loan_type == "Gold Loan":

            gold_weight = st.number_input(
                "🥇 Gold Weight (grams)",
                min_value=1.0,
                value=20.0,
                step=1.0,
            )

            gold_purity = st.selectbox(
                "Gold Purity",
                ["18K", "20K", "22K", "24K"],
            )

            loan_amount = st.number_input(
                "Required Gold Loan (₹)",
                min_value=1000,
                value=100000,
                step=5000,
            )

            st.caption(
                f"Gold entered: {gold_weight} grams, {gold_purity}. "
                "Actual valuation depends on bank assessment."
            )

        # ----------------------------------------------
        # OTHER LOANS
        # ----------------------------------------------

        else:

            minimum = product.get("min_amount")
            maximum = product.get("max_amount")

            minimum = int(minimum) if minimum is not None else 10000
            maximum = int(maximum) if maximum is not None else 100000000

            if maximum < minimum:
                st.error("The configured loan limits are invalid.")
                st.stop()

            default_amount = max(minimum, min(500000, maximum))

            loan_amount = st.number_input(
                "💰 Required Loan Amount (₹)",
                min_value=minimum,
                max_value=maximum,
                value=default_amount,
                step=10000,
            )

        # ----------------------------------------------
        # AMOUNT VALIDATION
        # ----------------------------------------------

        minimum = product.get("min_amount")
        maximum = product.get("max_amount")

        if minimum is not None and loan_amount < minimum:
            st.error(f"Minimum configured loan amount: ₹{minimum:,.0f}")
            valid_inputs = False

        if maximum is not None and loan_amount > maximum:
            st.error(f"Maximum configured loan amount: ₹{maximum:,.0f}")
            valid_inputs = False

        if loan_amount <= 0:
            st.error("Loan amount must be greater than zero.")
            valid_inputs = False

        # ----------------------------------------------
        # TENURE
        # ----------------------------------------------

        st.subheader("📅 Repayment Tenure")

        configured_tenure = product.get("max_tenure")

        if configured_tenure is not None:
            max_tenure = max(1, min(40, int(configured_tenure)))
        else:
            max_tenure = 30

        tenure = st.slider(
            "Select Tenure (Years)",
            min_value=1,
            max_value=max_tenure,
            value=min(5, max_tenure),
        )

        # ----------------------------------------------
        # INTEREST RATE
        # ----------------------------------------------

        configured_rate = product.get("interest_rate")

        if configured_rate is not None:
            interest_rate = float(configured_rate)

            st.info(
                f"Configured indicative rate: {interest_rate:.2f}%"
            )

        else:
            interest_rate = st.number_input(
                "📈 Enter Interest Rate (%)",
                min_value=0.0,
                max_value=50.0,
                value=10.0,
                step=0.1,
                help=(
                    "No numeric rate is configured for this product. "
                    "Enter a rate only after checking the bank's terms."
                ),
            )

        st.markdown("---")

        # ----------------------------------------------
        # ACTION BUTTONS
        # ----------------------------------------------

        b1, b2, b3 = st.columns(3)

        with b1:
            calculate = st.button(
                "🧮 Calculate EMI",
                type="primary",
                use_container_width=True,
            )

        with b2:
            official = st.button(
                "🌐 Official Website",
                use_container_width=True,
            )

        with b3:
            compare = st.button(
                "📊 Add to Compare",
                use_container_width=True,
            )

        if official:
            source_url = product.get("source_url") or BANK_WEBSITES.get(bank)

            if source_url:
                st.link_button(
                    "Open Bank Website",
                    source_url,
                )
            else:
                st.warning("No website URL is configured for this bank.")

        if compare:
            if not valid_inputs:
                st.error("Correct the loan details before saving.")
            else:
                item = {
                    "loan_type": loan_type,
                    "bank": bank,
                    "loan_amount": float(loan_amount),
                    "interest_rate": float(interest_rate),
                    "tenure_years": int(tenure),
                }

                add_comparison(item)

                st.success(
                    f"Added {bank} — {loan_type} to your comparisons."
                )

        if calculate:
            if not valid_inputs:
                st.error("Correct the loan details before calculating.")
            elif interest_rate < 0:
                st.error("Interest rate cannot be negative.")
            else:
                st.subheader("📊 Estimated EMI Results")

                show_emi_results(
                    loan_amount,
                    interest_rate,
                    tenure,
                )

                st.caption(
                    "This is an estimate, not a bank offer or approval. "
                    "Actual repayment may include fees, insurance and other charges."
                )

        st.markdown("---")

        st.caption(
            f"Information source: "
            f"{product.get('source', 'Bank information')}"
        )


# ==========================================================
# COMPARE LOANS PAGE
# ==========================================================

elif page == "📊 Compare Loans":

    st.title("📊 Compare Loans")

    st.write(
        "View saved loan estimates and compare available bank information."
    )

    saved_items = st.session_state.comparison_items

    st.subheader("📌 Your Saved Comparisons")

    if saved_items:

        rows = []

        for item in saved_items:
            emi, interest, total = safe_emi(
                item["loan_amount"],
                item["interest_rate"],
                item["tenure_years"],
            )

            rows.append({
                "Loan Type": item["loan_type"],
                "Bank": item["bank"],
                "Loan Amount": f"₹{item['loan_amount']:,.0f}",
                "Interest Rate": f"{item['interest_rate']:.2f}%",
                "Tenure": f"{item['tenure_years']} years",
                "Monthly EMI": f"₹{emi:,.2f}",
                "Total Interest": f"₹{interest:,.2f}",
                "Total Repayment": f"₹{total:,.2f}",
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

        remove_options = [
            f"{item['bank']} — {item['loan_type']}"
            for item in saved_items
        ]

        selected_remove = st.selectbox(
            "Select a saved comparison to remove",
            remove_options,
        )

        r1, r2 = st.columns(2)

        with r1:
            if st.button(
                "Remove Selected",
                use_container_width=True,
            ):
                index = remove_options.index(selected_remove)
                st.session_state.comparison_items.pop(index)
                st.rerun()

        with r2:
            if st.button(
                "Clear All Comparisons",
                use_container_width=True,
            ):
                st.session_state.comparison_items = []
                st.rerun()

    else:
        st.info(
            "No saved loans yet. Open Find Loan and click Add to Compare."
        )

    st.markdown("---")
    st.subheader("🏛️ Compare Bank Products")

    loan_type = st.selectbox(
        "Select Loan Category",
        list(LOAN_DATA.keys()),
        key="compare_loan_type",
    )

    selected_banks = st.multiselect(
        "Select at least two banks",
        BANKS,
        default=[
            bank for bank in ["SBI", "HDFC Bank", "ICICI Bank"]
            if bank in BANKS
        ],
        key="compare_banks",
    )

    if st.button(
        "Compare Selected Banks",
        type="primary",
        use_container_width=True,
    ):

        if len(selected_banks) < 2:
            st.warning("Please select at least two banks.")

        else:
            rows = []

            for bank in selected_banks:
                product = LOAN_DATA.get(loan_type, {}).get(bank)

                if product is None:
                    rows.append({
                        "Bank": bank,
                        "Availability": "No product data configured",
                        "Loan Amount": "-",
                        "Interest Rate": "-",
                        "Maximum Tenure": "-",
                    })
                else:
                    rows.append({
                        "Bank": bank,
                        "Availability": (
                            "Configured product information"
                        ),
                        "Loan Amount": get_amount_text(product),
                        "Interest Rate": get_rate_text(product),
                        "Maximum Tenure": get_tenure_text(product),
                    })

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True,
            )

    st.caption(
        "A listed product does not guarantee eligibility or approval. "
        "Verify current product details with the bank."
    )


# ==========================================================
# STANDALONE EMI CALCULATOR
# ==========================================================

elif page == "🧮 EMI Calculator":

    st.title("🧮 EMI Calculator")

    st.write(
        "Calculate an estimated monthly EMI for a loan."
    )

    amount = st.number_input(
        "💰 Loan Amount (₹)",
        min_value=1,
        max_value=100000000,
        value=500000,
        step=10000,
    )

    rate = st.number_input(
        "📈 Annual Interest Rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=10.0,
        step=0.1,
    )

    years = st.slider(
        "📅 Tenure (Years)",
        min_value=1,
        max_value=30,
        value=5,
    )

    if st.button(
        "🧮 Calculate EMI",
        type="primary",
        use_container_width=True,
    ):

        if amount <= 0:
            st.error("Loan amount must be greater than zero.")

        elif rate < 0:
            st.error("Interest rate cannot be negative.")

        else:
            st.subheader("📊 EMI Result")

            show_emi_results(
                amount,
                rate,
                years,
            )

            st.caption(
                "Estimate only. Actual bank repayments can differ."
            )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="footer">
        <div style="font-size:20px;font-weight:800;color:#0f172a;">
            🏦 SmartLoan India
        </div>
        <p>Compare • Calculate • Make informed decisions</p>
        <p>
            Loan information is provided for comparison and
            educational purposes only.
        </p>
        <p>
            Verify rates, eligibility, fees and terms with the
            respective bank before applying.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
