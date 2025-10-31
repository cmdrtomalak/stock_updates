# Next-Gen Stock Tracker

Modern stock tracking application using the latest versions of yfinance and pandas.

## Features

- **Daily Price Alerts**: Monitor stocks for significant daily price movements (>2% by default)
- **52-Week Low Alerts**: Get notified when stocks approach their 52-week lows
- **Bloomberg News**: Fetch and send top Bloomberg headlines
- **Discord Integration**: All alerts sent via Discord webhook

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Configure your Discord webhook URL in `.env`:
```bash
WEBHOOK_URL=your_discord_webhook_url_here
```

3. (Optional) Add index_names.txt file with stock symbols for 52-week low monitoring

## Usage

Run daily price updates (default):
```bash
uv run main.py
```

Run specific checks:
```bash
# Send Bloomberg headlines
uv run main.py --news

# Check daily price movements
uv run main.py --daily

# Check 52-week lows (only after market close)
uv run main.py --lows

# Run all checks
uv run main.py --all
```

## Configuration

### Monitored Stocks
Edit `STOCK_NAMES` in `stock_tracker.py` to change the watchlist:
```python
STOCK_NAMES = ["SPY", "QQQ", "DIS", "PDD", "UBER", "SHOP"]
```

### Alert Thresholds
Adjust thresholds in `stock_tracker.py`:
```python
DAILY_PERCENT_THRESHOLD = 2  # Daily movement threshold (%)
LOW_52_WEEK_PERCENT_THRESHOLD = 3  # 52-week low proximity (%)
```

### Excluded Publishers
Filter out news from certain publishers:
```python
EXCLUDED_PUBLISHERS = ["Benzinga", "Motley Fool", "TheStreet.com", "Business Insider"]
```

## Project Structure

```
next_gen/
├── main.py              # Main entry point with CLI
├── stock_tracker.py     # Core stock tracking functionality
├── get_bloomberg.py     # Bloomberg news scraper
├── pyproject.toml       # Project dependencies (uv)
├── .env                 # Environment variables (not in git)
├── index_names.txt      # S&P 500 symbols for 52-week checks
└── nasdaq_names.txt     # NASDAQ symbols
```

## Improvements over Original

- Modern Python 3.13 with type hints
- Using `uv` for faster dependency management
- Updated to latest pandas (2.3.3) and yfinance (0.2.66)
- Using `zoneinfo` instead of `pytz` for timezone handling
- Modular design with separate concerns
- CLI argument parser for flexible execution
- Better error handling and logging
- Cleaner code structure and documentation
