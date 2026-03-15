import html
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

MAIL_PASSWORD_FILE = Path.home() / ".pilot_one_mail_password"
ACTION_HINTS = ("watch", "monitor", "review", "follow", "confirm", "check", "track", "prepare")


def _require_env(name):
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing {name} in .env.")
    return value


def _resolve_mail_password():
    value = os.getenv("MAIL_PASSWORD", "").strip()
    if value:
        return value

    if MAIL_PASSWORD_FILE.exists():
        secret = MAIL_PASSWORD_FILE.read_text(encoding="utf-8").strip()
        if secret:
            return secret

    raise ValueError("Missing MAIL_PASSWORD. Set it in the environment or in the hidden user secret file.")


def _build_action_items(company, content):
    sentences = [part.strip(" .") for part in content.replace("\n", " ").split(".") if part.strip()]
    actions = []

    for sentence in sentences:
        lowered = sentence.lower()
        if any(hint in lowered for hint in ACTION_HINTS):
            actions.append(sentence)
        if len(actions) == 3:
            break

    if not actions:
        actions = [
            f"Review whether the latest {company} development affects your priorities.",
            f"Monitor follow-up coverage for {company} over the next reporting cycle.",
        ]

    return actions[:3]


def _build_plain_text(company, summary, action_items):
    lines = [
        f"Report for {company}",
        "",
        summary,
        "",
        "Suggested next actions:",
    ]
    lines.extend([f"- {item}" for item in action_items])
    return "\n".join(lines)


def _build_html(company, summary, action_items):
    actions_html = "".join(f"<li>{html.escape(item)}</li>" for item in action_items)
    return (
        f"<h3>Report for <strong>{html.escape(company)}</strong></h3>"
        f"<p>{html.escape(summary)}</p>"
        "<h4>Suggested next actions</h4>"
        f"<ul>{actions_html}</ul>"
    )


def send_brief(to_email, company, content, action_items=None):
    clean_content = content.strip()
    if not clean_content:
        raise ValueError("Cannot send an email with an empty summary.")

    safe_company = company.strip()
    subject = f"Briefing: {safe_company}"
    sender = _require_env("MAIL_DEFAULT_SENDER")
    username = _require_env("MAIL_USERNAME")
    password = _resolve_mail_password()
    server = _require_env("MAIL_SERVER")
    port = int(os.getenv("MAIL_PORT", "587"))
    use_tls = os.getenv("MAIL_USE_TLS", "true").strip().lower() == "true"
    resolved_actions = [item.strip() for item in (action_items or _build_action_items(safe_company, clean_content)) if item.strip()][:3]

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = to_email
    message.set_content(_build_plain_text(safe_company, clean_content, resolved_actions))
    message.add_alternative(_build_html(safe_company, clean_content, resolved_actions), subtype="html")

    with smtplib.SMTP(server, port, timeout=30) as smtp:
        if use_tls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(message)

    return {"status": "sent", "to": to_email, "subject": subject}
