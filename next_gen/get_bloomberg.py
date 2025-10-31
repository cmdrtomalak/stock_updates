"""Fetch Bloomberg headlines from Google News RSS feed."""
import requests
from bs4 import BeautifulSoup


def get_bloomberg_headlines(limit: int = 5) -> list[tuple[str, str]]:
    """
    Fetch recent Bloomberg headlines from Google News RSS feed.
    
    Args:
        limit: Maximum number of headlines to return
        
    Returns:
        List of tuples containing (title, link)
    """
    rss_feed = "https://news.google.com/rss/search?q=when:2h+allinurl:bloomberg.com&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(rss_feed, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "xml")
        items = soup.find_all("item")
        
        headlines = []
        for item in items[:limit]:
            title = item.title.get_text() if item.title else "No title"
            link = item.link.get_text() if item.link else ""
            headlines.append((title, link))
        
        return headlines
    except requests.RequestException as e:
        print(f"Error fetching Bloomberg headlines: {e}")
        return []


if __name__ == '__main__':
    headlines = get_bloomberg_headlines()
    for i, (title, link) in enumerate(headlines, 1):
        print(f"{i}. {title}")
        print(f"   {link}\n")
