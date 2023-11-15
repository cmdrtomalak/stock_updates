#!/home/bandit/stock_updates/venv/bin/python3
import requests
import os
import yfinance as yf

webhook_url = os.getenv("WEBHOOK_URL")

STOCK_NAMES = ["SPY", "QQQ", "DIS"]
COMPANY_NAMES = ["S&P 500", "Nasdaq", "Disney"]

DAILY_PERCENT_THRESHOLD = 2
LOW_52_WEEK_PERCENT_THRESHOLD = 3

def get_current_price(instrument):
    data = yf.Ticker(instrument).history(period="1d", interval="1m")
    
    if not data.empty:
        return data['Close'].iloc[-1]
    else:
        return None


def get_previous_close(instrument):
    data = yf.Ticker(instrument).history(period="1wk", interval="1d")
    
    if not data.empty:
        return data['Close'].iloc[-2]
    else:
        return None


def get_52_wk_low(instrument):
    data = yf.Ticker(instrument).history(period='1y', interval='1d')

    if not data.empty:
        return data["Low"].min()
    else:
        return None
       

def get_top_3_news(ticker):
    stock_news = yf.Ticker(ticker).news
    
    return stock_news[:3] 


def send_daily_updates(instrument, curr_px, prev_clse):
    price_difference = curr_px - prev_clse
    price_difference_abs = abs(curr_px - prev_clse)

    percentage_change = price_difference / prev_clse * 100
    percentage_change_abs = price_difference_abs / prev_clse * 100

    if percentage_change_abs > DAILY_PERCENT_THRESHOLD:
        
        three_articles = get_top_3_news(instrument)

        formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['link']}" for article in three_articles]
        # print(formatted_articles)

        up_down = ''
        up_down_color = '1127128'
        if percentage_change > 0.0:
            up_down = '🔺'
            up_down_color = '52224'
        else:
            up_down = '🔻'
            up_down_color = '13369344'

        for article in formatted_articles:
            payload = {
                    "content": "Hourly Market Update",
                    "username": "Money Bot",
                    "embeds": [
                        {
                            "title": f"Price Alert: {instrument}: {up_down} {round(percentage_change, 2)}",
                            "description": f"{article}",
                            "color": up_down_color
                            }
                        ]
                    }
            headers = {
                    "Content-Type": "application/json"
                    }
            response = requests.post(webhook_url, json=payload, headers=headers)

            if response.status_code == 204:
                print("Message sent successfully.")
            else:
                print(f"Failed to send message: {response.status_code}, {response.text}")


def send_52_week_lows(instrument, curr_px, low_52_wk):
    price_difference = curr_px - low_52_wk
    price_difference_abs = abs(curr_px - low_52_wk)

    percentage_change = price_difference / low_52_wk * 100
    percentage_change_abs = price_difference_abs / low_52_wk * 100

    percentage_change_abs = 2
    if percentage_change_abs < LOW_52_WEEK_PERCENT_THRESHOLD:
        payload = {
                "content": "52 Week Low Alert",
                "username": "Money Bot",
                "embeds": [
                    {
                        "title": f"{instrument} Alert: ",
                        "description": f"Current Price {round(curr_px, 2)} is within {round(percentage_change, 2)} of 52 Week low of {round(low_52_wk, 2)}",
                        "color": 5832883
                        }
                    ]
                }
        headers = {
                "Content-Type": "application/json"
                }
        response = requests.post(webhook_url, json=payload, headers=headers)

        if response.status_code == 204:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message: {response.status_code}, {response.text}")



if __name__ == '__main__':
    for (i, instrument) in enumerate(STOCK_NAMES):
        current_px = get_current_price(instrument)
        previous_close = get_previous_close(instrument)
        low_52_wk = get_52_wk_low(instrument)

        # print(f"Current Price: {current_px}")
        # print(f"Previous Price: {previous_close}")
        # print(f"52 Week Low: {low_52_wk}")

        # send_daily_updates(instrument, current_px, previous_close)
        send_52_week_lows(instrument, current_px, low_52_wk)

