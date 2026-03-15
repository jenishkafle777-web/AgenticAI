def search_news(company, topic=""):
    topic = topic.strip()
    if topic:
        query = f"{company} {topic}"
        return f"Found top 3 news for {query}..."
    return f"Found top 3 news for {company}..."
