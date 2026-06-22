def remove_duplicates(news):
    seen = set()
    unique_news = []
    for article in news:
        title = article.get("title", "").strip()

        if title not in seen:
            seen.add(title)
            unique_news.append(article)
    return unique_news