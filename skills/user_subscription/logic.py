import json
import os


def _normalize_subscription(entry):
    return {
        "email": entry.get("email", "").strip(),
        "company": entry.get("company", "").strip(),
        "topic": entry.get("topic", "").strip(),
        "frequency": entry.get("frequency", "").strip(),
    }


def _dedupe_subscriptions(entries):
    deduped = []
    seen = set()
    for entry in entries:
        normalized = _normalize_subscription(entry)
        key = tuple(normalized.values())
        if key not in seen:
            seen.add(key)
            deduped.append(normalized)
    return deduped


def save_subscription(email, company, topic, frequency):
    data = _normalize_subscription(
        {
            "email": email,
            "company": company,
            "topic": topic,
            "frequency": frequency,
        }
    )
    file_path = "subscriptions.json"

    # Load existing or start new list
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            masters = _dedupe_subscriptions(json.load(f))
    else:
        masters = []

    if data in masters:
        with open(file_path, "w") as f:
            json.dump(masters, f, indent=4)
        return "Subscription already exists!"

    masters.append(data)
    with open(file_path, "w") as f:
        json.dump(masters, f, indent=4)
    return "Subscription Saved!"
