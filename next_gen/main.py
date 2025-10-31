#!/usr/bin/env python3
"""
Next-gen stock tracking application using modern yfinance and pandas.
Monitors stock prices and sends alerts via Discord webhook.
"""
import argparse
from datetime import datetime

import get_bloomberg
from stock_tracker import (
    STOCK_NAMES,
    get_current_price,
    get_previous_close,
    get_52_week_low,
    send_daily_updates,
    send_52_week_low_alert,
    send_discord_message,
    load_index_symbols,
    is_market_closed,
)


def send_top_news(limit: int = 5) -> None:
    """Send top Bloomberg headlines to Discord."""
    print(f"\nFetching top {limit} Bloomberg headlines...")
    headlines = get_bloomberg.get_bloomberg_headlines(limit)
    
    for title, link in headlines:
        send_discord_message(
            title=title,
            description=link,
            color=1738906  # Blue color
        )


def run_daily_updates() -> None:
    """Monitor watchlist for daily price movements."""
    print(f"\nStarting daily updates at {datetime.now()}")
    
    for symbol in STOCK_NAMES:
        print(f"\nChecking {symbol}...")
        current_price = get_current_price(symbol)
        previous_close = get_previous_close(symbol)
        
        if current_price is not None and previous_close is not None:
            print(f"  Current: ${current_price:.2f}, Previous Close: ${previous_close:.2f}")
            send_daily_updates(symbol, current_price, previous_close)
        else:
            print(f"  Unable to fetch prices for {symbol}")


def run_52_week_low_checks() -> None:
    """Check 52-week lows for index symbols (typically after market close)."""
    if not is_market_closed():
        print("\nMarket still open - skipping 52-week low checks")
        return
    
    print("\nMarket closed - checking 52-week lows...")
    index_symbols = load_index_symbols('index_names.txt')
    
    if not index_symbols:
        print("No index symbols loaded")
        return
    
    print(f"Checking {len(index_symbols)} symbols for 52-week lows...")
    checked = 0
    for symbol in index_symbols:
        current_price = get_current_price(symbol)
        low_52_week = get_52_week_low(symbol)
        
        if current_price is not None and low_52_week is not None:
            send_52_week_low_alert(symbol, current_price, low_52_week)
        
        checked += 1
        if checked % 50 == 0:
            print(f"  Checked {checked}/{len(index_symbols)} symbols...")
    
    print(f"Completed checking {checked} symbols")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Stock tracker with price alerts and news updates"
    )
    parser.add_argument(
        '--news',
        action='store_true',
        help='Send top Bloomberg headlines'
    )
    parser.add_argument(
        '--daily',
        action='store_true',
        help='Run daily price movement checks'
    )
    parser.add_argument(
        '--lows',
        action='store_true',
        help='Check for 52-week lows'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all checks (news, daily updates, and 52-week lows)'
    )
    
    args = parser.parse_args()
    
    # If no specific flags, run daily updates AND 52-week lows (matching original behavior)
    if not any([args.news, args.daily, args.lows, args.all]):
        args.daily = True
        args.lows = True
    
    print("=" * 60)
    print("Next-Gen Stock Tracker")
    print("=" * 60)
    
    if args.all or args.news:
        send_top_news()
    
    if args.all or args.daily:
        run_daily_updates()
    
    if args.all or args.lows:
        run_52_week_low_checks()
    
    print("\n" + "=" * 60)
    print("Stock tracker completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
