import os

from dotenv import load_dotenv

from skills.email_delivery.logic import send_brief
from skills.home_mortgage.logic import MortgageInputs, build_true_cost_model
from skills.news_search.logic import search_news
from skills.user_subscription.logic import save_subscription

load_dotenv()


def _build_company_label(company, topic):
    if topic:
        return f"{company} ({topic})"
    return company


def _confirm_execution(user_email, company, topic, freq):
    print("\nPlease confirm your request:")
    print(f"- Recipient email: {user_email}")
    print(f"- Company to monitor: {company}")
    print(f"- Topic or keyword: {topic or 'Any relevant company news'}")
    print(f"- Email frequency: {freq}")
    confirmation = input("Type 'yes' to continue or anything else to cancel: ").strip().lower()
    return confirmation == "yes"


def run_news_agent_loop():
    print("--- News Pilot Agent Started ---")

    # 1. Capture User Intent
    user_email = input("Enter your email: ")
    company = input("Which company should I monitor? ")
    topic = input("Any specific keyword or topic to track? ").strip()
    freq = input("Frequency (Daily/Weekly)? ")

    if not _confirm_execution(user_email, company, topic, freq):
        print("Request cancelled. No subscription saved and no email sent.")
        return

    # 2. Save Subscription
    subscription_result = save_subscription(user_email, company, topic, freq)
    print(f"{subscription_result} {user_email} -> {_build_company_label(company, topic)} ({freq})")

    # 3. Execute Search (The 'Work')
    print("Researching...")
    news_content = search_news(company, topic)

    # 4. Deliver Result
    print("Dispatching email...")
    send_brief(user_email, _build_company_label(company, topic), news_content)

    print("--- Task Complete ---")


def _read_float(prompt, default=None):
    raw = input(prompt).strip()
    if not raw and default is not None:
        return float(default)
    return float(raw)


def _read_int(prompt, default=None):
    raw = input(prompt).strip()
    if not raw and default is not None:
        return int(default)
    return int(raw)


def _fmt_currency(value):
    return f"${value:,.2f}"


def _print_mortgage_report(model):
    monthly = model["monthly_breakdown"]

    print("\n=== US Home Mortgage & True Monthly Cost Model ===")
    print(f"Loan Amount: {_fmt_currency(model['loan_amount'])}")
    print("\nMonthly Payment Breakdown (P.I.T.I. +)")
    print(f"- Principal & Interest: {_fmt_currency(monthly['principal_interest'])}")
    print(f"- Property Taxes: {_fmt_currency(monthly['property_tax'])}")
    print(f"- Home Insurance: {_fmt_currency(monthly['home_insurance'])}")
    print(f"- PMI: {_fmt_currency(monthly['pmi'])}")
    print(f"- HOA: {_fmt_currency(monthly['hoa'])}")
    print(f"- Maintenance: {_fmt_currency(monthly['maintenance'])}")
    print(f"- Total Monthly Ownership Cost: {_fmt_currency(monthly['total_monthly_cost'])}")

    print("\nAmortization Snapshot (First 12 Months)")
    print("Month | Opening Balance | Interest | Principal | Ending Balance")
    for row in model["amortization_first_12"]:
        print(
            f"{row.month:>5} | {_fmt_currency(row.opening_balance):>15} | {_fmt_currency(row.interest_paid):>9} | "
            f"{_fmt_currency(row.principal_paid):>10} | {_fmt_currency(row.ending_balance):>13}"
        )

    print("\nMulti-Rate Comparison")
    print("Rate | Monthly P&I | Total Monthly (Tax+Ins) | Total Interest")
    for option in model["rate_comparison"]:
        print(
            f"{option['rate']:>4.2f}% | {_fmt_currency(option['monthly_pi']):>11} | "
            f"{_fmt_currency(option['total_monthly_tax_ins']):>24} | {_fmt_currency(option['total_interest']):>14}"
        )

    print("\nUS Buyer Pro Tips")
    print(f"- 1.25% Rule estimate: {_fmt_currency(model['rule_of_thumb_1_25_pct'])} / month")
    print(f"- PMI cancellation request at 80% LTV around month: {model['pmi_cancel_80_month']}")
    print(f"- PMI automatic removal at 78% LTV around month: {model['pmi_auto_remove_78_month']}")


def run_mortgage_agent_loop():
    print("--- US Mortgage Cost Agent ---")

    inputs = MortgageInputs(
        home_price=_read_float("Home purchase price (e.g. 500000): "),
        down_payment_pct=_read_float("Down payment % (e.g. 20): "),
        annual_interest_rate=_read_float("Annual interest rate % (e.g. 6.5): "),
        term_years=_read_int("Loan term in years (default 30): ", default=30),
        property_tax_rate=_read_float("Property tax rate % (default 1.2): ", default=1.2),
        annual_home_insurance=_read_float("Annual home insurance premium (default 1800): ", default=1800),
        pmi_rate=_read_float("PMI annual rate % (default 1.0): ", default=1.0),
        hoa_monthly=_read_float("Monthly HOA fee (default 0): ", default=0),
        maintenance_monthly=_read_float("Monthly maintenance budget (default 0): ", default=0),
    )

    model = build_true_cost_model(inputs)
    _print_mortgage_report(model)


def run_agent():
    print("Choose an agent:")
    print("1) Corporate news intelligence")
    print("2) US mortgage ownership cost model")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        run_news_agent_loop()
    elif choice == "2":
        run_mortgage_agent_loop()
    else:
        print("Invalid option. Please run again and choose 1 or 2.")


if __name__ == "__main__":
    run_agent()
