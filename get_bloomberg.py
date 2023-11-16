# Import the libraries
import requests
from bs4 import BeautifulSoup

def get_bloomberg_headlines():
    news_stories = []
    # Define the RSS feed to scrape
    rss_feed = "https://news.google.com/rss/search?q=when:2h+allinurl:bloomberg.com&hl=en-US&gl=US&ceid=US:en"

    # Get the XML content of the RSS feed
    response = requests.get(rss_feed)
    # Parse the XML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "xml")
    # Find all the items that contain the headlines and links
    items = soup.find_all("item")
    # Loop through each item
    for item in items:
        # Get the text content of the title element
        title = item.title.get_text()
        # Get the text content of the link element
        link = item.link.get_text()

        news_stories.append((title, link))

    return news_stories
