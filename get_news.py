# Import the libraries
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_stories():
    # Define the news websites to scrape
    news_websites = ["https://www.cnbc.com/finance/", "https://finance.yahoo.com/news", "https://www.cnn.com/BUSINESS", "https://www.theguardian.com/uk/business", "https://www.usatoday.com/money/"]

    # Create an empty list to store the news stories
    news_stories = []

    # Loop through each news website
    for website in news_websites:
        # Get the HTML content of the website
        response = requests.get(website)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        # Find all the elements that contain the headlines and snippets
        elements = soup.find_all(["h1", "h2", "h3", "p"])
        # Loop through each element
        for element in elements:
            # Get the text content of the element
            text = element.get_text().strip()
            # Get the link of the element if it has one
            link = element.find("a")["href"] if element.find("a") else None
            # If the text and the link are not empty, add them to the news stories list
            if text and link:
                news_stories.append((text, link))

    return news_stories


# Define a function to get the date of a news story from its link
def get_date(link):
    # Try to parse the link using the datetime library
    try:
        date = datetime.strptime(link, "%Y/%m/%d/%H/%M/%S")
    # If the link does not have a date format, return the current date
    except ValueError:
        date = datetime.now()
    # Return the date
    return date


def get_top_news():
    news_stories = get_stories()

    # Sort the news stories by the date in descending order
    news_stories.sort(key=lambda x: get_date(x[1]), reverse=True)

    return news_stories
