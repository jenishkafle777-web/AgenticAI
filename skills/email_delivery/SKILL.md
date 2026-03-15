---
name: email-delivery
description: Formats and sends intelligence briefs via Gmail SMTP.
---
# Guardrails
1. Never send an email if the 'summary' field is empty.
2. Ensure the 'subject' line includes the company name.
3. Format the body using clean HTML and include a concise "Suggested next actions" section when the update implies follow-up work.
4. Read all SMTP settings from `.env`; never hardcode credentials in code.
5. Keep the brief concise, but do not enforce a rigid character or word cap unless the user requests one.

# Metadata Requirements
- recipient_email: Valid email string
- company_name: String
- summary: String
- action_items: Optional list of up to 3 concise next steps for the user
