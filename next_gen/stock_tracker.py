#!/usr/bin/env python3
"""
Modern stock tracking script using latest yfinance and pandas.
Monitors stock price movements and sends alerts via Discord webhook.
"""
import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import yfinance as yf
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

STOCK_NAMES = ["SPY", "QQQ", "DIS", "PDD", "UBER", "SHOP", "CMG", "SG"]
COMPANY_NAMES = ["S&P 500", "Nasdaq", "Disney", "Pinduoduo", "Uber", "Shopify", "Chipotle", "Sweetgreens"]
EXCLUDED_PUBLISHERS = ["Benzinga", "Motley Fool", "TheStreet.com", "Business Insider"]

DAILY_PERCENT_THRESHOLD = 2
LOW_52_WEEK_PERCENT_THRESHOLD = 3


def get_current_price(symbol: str) -> float | None:
    """Get the most recent price for a symbol using 1-minute interval data."""
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")
    
    if not data.empty:
        return float(data['Close'].iloc[-1])
    return None


def get_previous_close(symbol: str) -> float | None:
    """Get the previous day's closing price for a symbol."""
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="5d", interval="1d")
    
    if len(data) >= 2:
        return float(data['Close'].iloc[-2])
    return None


def get_52_week_low(symbol: str) -> float | None:
    """Get the 52-week low price for a symbol."""
    ticker = yf.Ticker(symbol)
    info = ticker.info
    return info.get('fiftyTwoWeekLow')


def get_top_news(symbol: str, limit: int = 3) -> list[dict]:
    """Get top news articles for a symbol, filtering out excluded publishers."""
    ticker = yf.Ticker(symbol)
    stock_news = ticker.news
    
    processed_news = []
    for news_item in stock_news:
        content = news_item.get('content', {})
        
        # Safely extract link from nested structure
        link = 'No link available'
        click_through = content.get('clickThroughUrl')
        if click_through and isinstance(click_through, dict):
            link = click_through.get('url', link)
        else:
            canonical = content.get('canonicalUrl')
            if canonical and isinstance(canonical, dict):
                link = canonical.get('url', link)
        
        # Extract relevant fields from the nested content structure
        article = {
            'title': content.get('title', 'No title available'),
            'publisher': content.get('provider', {}).get('displayName', 'Unknown'),
            'link': link
        }
        
        # Filter out excluded publishers
        if article['publisher'] not in EXCLUDED_PUBLISHERS:
            processed_news.append(article)
    
    return processed_news[:limit]


def send_discord_message(title: str, description: str, color: int) -> bool:
    """Send a message to Discord via webhook."""
    if not WEBHOOK_URL:
        print("Warning: WEBHOOK_URL not configured")
        return False
        
    payload = {
        "content": "",
        "username": "Money Bot",
        "embeds": [{
            "title": title,
            "description": description,
            "color": color
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    
    if response.status_code == 204:
        print(f"Message sent: {title}")
        return True
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")
        return False


def send_daily_updates(symbol: str, current_price: float, previous_close: float) -> None:
    """Send price alerts if daily change exceeds threshold."""
    price_change = current_price - previous_close
    percent_change = (price_change / previous_close) * 100
    
    if abs(percent_change) > DAILY_PERCENT_THRESHOLD:
        news_articles = get_top_news(symbol)
        
        up_down = '🔺' if percent_change > 0 else '🔻'
        color = 52224 if percent_change > 0 else 13369344
        
        title = f"Price Alert: {symbol}: {up_down} {percent_change:.2f}%"
        
        for article in news_articles:
            description = (
                f"Headline: {article.get('title', 'No title available')}\n"
                f"Publisher: {article.get('publisher', 'Unknown')}\n"
                f"Link: {article.get('link', 'No link available')}"
            )
            send_discord_message(title, description, color)


def send_52_week_low_alert(symbol: str, current_price: float, low_52_week: float) -> None:
    """Send alert if price is near 52-week low."""
    price_change = current_price - low_52_week
    percent_from_low = (price_change / low_52_week) * 100
    
    if abs(percent_from_low) < LOW_52_WEEK_PERCENT_THRESHOLD:
        title = f"{symbol} Alert: Near 52-Week Low"
        description = (
            f"Current Price ${current_price:.2f} is within {percent_from_low:.2f}% "
            f"of 52 Week low of ${low_52_week:.2f}"
        )
        send_discord_message(title, description, 5832883)


def load_index_symbols(filename: str) -> list[str]:
    """Load stock symbols from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
        return []


def is_market_closed() -> bool:
    """Check if US market is closed (after 4:00 PM ET)."""
    eastern_tz = ZoneInfo('America/New_York')
    current_time = datetime.now(eastern_tz).time()
    market_close = datetime.strptime("16:00:00", "%H:%M:%S").time()
    return current_time >= market_close


def main():
    """Main execution function."""
    print(f"Starting stock tracker at {datetime.now()}")
    
    # Monitor watchlist for daily price movements
    for symbol in STOCK_NAMES:
        print(f"\nChecking {symbol}...")
        current_price = get_current_price(symbol)
        previous_close = get_previous_close(symbol)
        
        if current_price is not None and previous_close is not None:
            print(f"  Current: ${current_price:.2f}, Previous Close: ${previous_close:.2f}")
            send_daily_updates(symbol, current_price, previous_close)
        else:
            print(f"  Unable to fetch prices for {symbol}")
    
    # Check 52-week lows after market close
    if is_market_closed():
        print("\nMarket closed - checking 52-week lows...")
        index_symbols = load_index_symbols('index_names.txt')
        
        for symbol in index_symbols:
            current_price = get_current_price(symbol)
            low_52_week = get_52_week_low(symbol)
            
            if current_price is not None and low_52_week is not None:
                send_52_week_low_alert(symbol, current_price, low_52_week)
    
    print("\nStock tracker completed")


if __name__ == '__main__':
    main()
