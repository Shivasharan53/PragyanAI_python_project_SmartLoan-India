
import streamlit as st
import pandas as pd

from loan_data import BANKS
from loan_calculator import calculate_loan_summary

st.set_page_config(
    page_title="SmartLoan India",
    page_icon="🏦",
    layout="wide",
)

# -------------------- SESSION STATE --------------------
if "bank" not in st.session_state:
    st.session_state.bank = next(iter(BANKS))

if "product" not in st.session_state:
    st.session_state.product = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# -------------------- STYLING --------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.hero {
    padding: 28px;
    border-radius: 16px;
    background: linear-gradient(120deg, #102D50, #167D9A);
    color: white;
}
.hero h1 { color: white; }
.hero p { color: #E5F4FF; }
div[data-testid="stMetric"] {
    border: 1px solid #D7E1EB;
    border-radius: 12px;
    padding: 14px;
}
</style>
""", unsafe_allow_html=True)


def money(value):
    return f"₹{value:,.2f}"


def navigate(page):
    st.session_state.page = page
    st.rerun()


def open_bank(bank_name):
    st.session_state.bank = bank_name
    st.session_state.product = ""
    navigate("Explore Banks")


def show_product(bank_name, category, product):
    st.subheader(f"{bank_name} — {category}")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Loan purpose")
        st.write(product["purpose"])

        st.markdown("#### Eligibility")
        st.write(product["eligibility"])

    with right:
        st.markdown("#### Required documents")
        st.write(product["documents"])

        st.markdown("#### Interest rate")
        st.info(product["rate"])

    st.link_button(
        "🌐 Open Official Product Website",
        product["url"],
        use_container_width=True,
    )

    st.caption(
        "Confirm product availability, interest rates, fees and terms "
        "on the official provider website before applying."
    )


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("🏦 SmartLoan India")
    st.caption("Explore • Compare • Calculate")

    pages = [
        "Dashboard",
        "Explore Banks",
        "Compare Loans",
        "EMI Calculator",
        "Insurance",
        "About",
    ]

    selected_page = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.page),
    )

    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    st.divider()
    st.caption("Loan information and EMI estimates only.")

page = st.session_state.page

# -------------------- DASHBOARD --------------------
if page == "Dashboard":
    st.markdown("""
    <div class="hero">
        <h1>SmartLoan India</h1>
        <p>Explore banks, discover loan products and calculate your EMI.</p>
    </div>
    """, unsafe_allow_html=True)

    total_products = sum(
        len(bank["products"]) for bank in BANKS.values()
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Banks listed", len(BANKS))
    c2.metric("Loan entries", total_products)
    c3.metric("Tools available", 3)

    st.divider()
    st.subheader("🏦 Choose Your Bank")

    bank_names = list(BANKS.keys())

    for start in range(0, len(bank_names), 3):
        cols = st.columns(3)

        for col, name in zip(cols, bank_names[start:start + 3]):
            with col:
                st.markdown(f"### {name}")
                st.write(
                    f"{len(BANKS[name]['products'])} listed loan categories"
                )

                if st.button(
                    "Explore Bank →",
                    key=f"dashboard_{name}",
                    use_container_width=True,
                ):
                    open_bank(name)

    st.divider()
    st.subheader("⚡ Quick Actions")

    a, b, c = st.columns(3)

    with a:
        if st.button("📊 Compare Loans", use_container_width=True):
            navigate("Compare Loans")

    with b:
        if st.button("🧮 Calculate EMI", use_container_width=True):
            navigate("EMI Calculator")

    with c:
        if st.button("🛡️ Explore Insurance", use_container_width=True):
            navigate("Insurance")

# -------------------- EXPLORE BANKS --------------------
elif page == "Explore Banks":
    st.title("🏦 Explore Banks")
    st.write("Click a bank, then click any listed loan product.")

    bank_names = list(BANKS.keys())

    for start in range(0, len(bank_names), 3):
        cols = st.columns(3)

        for col, name in zip(cols, bank_names[start:start + 3]):
            with col:
                label = f"✓ {name}" if name == st.session_state.bank else name

                if st.button(
                    label,
                    key=f"bank_select_{name}",
                    use_container_width=True,
                ):
                    st.session_state.bank = name
                    st.session_state.product = ""
                    st.rerun()

    bank_name = st.session_state.bank
    bank = BANKS[bank_name]

    st.divider()
    left, right = st.columns([3, 1])

    with left:
        st.subheader(bank_name)
        st.write("Select a category to view its information.")

    with right:
        st.link_button(
            "Official Bank Website ↗",
            bank["website"],
            use_container_width=True,
        )

    product_names = list(bank["products"].keys())

    st.subheader("Available Loan Categories")

    for start in range(0, len(product_names), 2):
        cols = st.columns(2)

        for col, category in zip(
            cols, product_names[start:start + 2]
        ):
            with col:
                if st.button(
                    f"📄 {category}",
                    key=f"category_{bank_name}_{category}",
                    use_container_width=True,
                ):
                    st.session_state.product = category
                    st.rerun()

    category = st.session_state.product

    if category in bank["products"]:
        st.divider()
        show_product(bank_name, category, bank["products"][category])
    else:
        st.info("Select a product button above to see the details.")

# -------------------- COMPARE LOANS --------------------
elif page == "Compare Loans":
    st.title("📊 Compare Loan Products")

    records = []

    for bank_name, bank in BANKS.items():
        for category, product in bank["products"].items():
            records.append({
                "Bank": bank_name,
                "Category": category,
                "Purpose": product["purpose"],
                "Eligibility": product["eligibility"],
                "Rate information": product["rate"],
                "Official website": product["url"],
            })

    df = pd.DataFrame(records)

    selected_banks = st.multiselect(
        "Select banks",
        options=list(BANKS),
        default=list(BANKS),
    )

    all_categories = sorted(df["Category"].unique())

    selected_categories = st.multiselect(
        "Select loan categories",
        options=all_categories,
        default=all_categories,
    )

    filtered = df[
        df["Bank"].isin(selected_banks)
        & df["Category"].isin(selected_categories)
    ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Official website": st.column_config.LinkColumn(
                "Official website",
                display_text="Open official page",
            )
        },
    )

    st.download_button(
        "⬇️ Download Comparison CSV",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="smartloan_comparison.csv",
        mime="text/csv",
    )

# -------------------- EMI CALCULATOR --------------------
elif page == "EMI Calculator":
    st.title("🧮 Loan EMI Calculator")
    st.write("Calculate an estimated monthly EMI.")

    with st.form("emi_form"):
        principal = st.number_input(
            "Loan amount (₹)",
            min_value=1000,
            max_value=100000000,
            value=500000,
            step=10000,
        )

        rate = st.number_input(
            "Annual interest rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=9.0,
            step=0.25,
        )

        years = st.number_input(
            "Loan tenure (years)",
            min_value=1,
            max_value=40,
            value=5,
            step=1,
        )

        submitted = st.form_submit_button(
            "Calculate EMI",
            use_container_width=True,
        )

    if submitted:
        result = calculate_loan_summary(principal, rate, years)

        c1, c2, c3 = st.columns(3)

        c1.metric("Monthly EMI", money(result["monthly_emi"]))
        c2.metric("Total interest", money(result["total_interest"]))
        c3.metric("Total repayment", money(result["total_payment"]))

        st.caption(
            "Estimate only. Actual lender calculations may include fees, "
            "insurance or other charges."
        )

# -------------------- INSURANCE --------------------
elif page == "Insurance":
    st.title("🛡️ Insurance Explorer")

    st.write(
        "Insurance is a protection product, not a loan. "
        "Check the actual insurer and policy details before purchasing."
    )

    insurance_types = [
        "Life Insurance",
        "Health Insurance",
        "Bike Insurance",
        "Car Insurance",
        "Home Insurance",
        "Student Insurance",
    ]

    category = st.selectbox(
        "Select insurance category",
        insurance_types,
    )

    st.subheader(category)

    st.write(
        "Coverage, exclusions, premiums and eligibility depend on "
        "the insurer and the specific policy."
    )

    st.info(
        "Use the official insurer's product page to confirm the policy. "
        "The bank homepage is provided as a starting point, not as proof "
        "that a particular insurance product is available."
    )

    for bank_name, bank in BANKS.items():
        st.markdown(f"**{bank_name}**")

        st.link_button(
            f"Visit {bank_name} Website ↗",
            bank["insurance_url"],
            key=f"insurance_link_{bank_name}",
        )

# -------------------- ABOUT --------------------
elif page == "About":
    st.title("ℹ️ About SmartLoan India")

    st.markdown("""
    SmartLoan India is a banking information and loan calculation
    dashboard built using Python and Streamlit.

    **Features**
    - Bank selection and product details
    - Official website links
    - Loan comparison and CSV export
    - EMI, interest and repayment calculations
    - Separate insurance information section

    **Disclaimer:** This app does not approve loans, sell insurance or
    guarantee product availability. Confirm current rates, fees,
    eligibility and policy conditions with the official provider.
    """)
