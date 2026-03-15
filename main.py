import os

from dotenv import load_dotenv

from skills.email_delivery.logic import send_brief
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


def run_pilot_loop():
    print("---  Pilot Agent Started ---")

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
    # In a real run, news_content would be the AI summary
    send_brief(user_email, _build_company_label(company, topic), news_content)

    print("--- Task Complete ---")


if __name__ == "__main__":
    run_pilot_loop()
