Simple script to get daily stock updates and run screens

Sends updates to a Discord using webhook_url. Setup a .env file with WEBHOOK_URL defined for your webhook.

To run you need to swap out the current main version of yfinance with the branch feature/cookie-and-crumb due to https://github.com/ranaroussi/yfinance/issues/1729, a possible resolution is https://github.com/ranaroussi/yfinance/pull/1657

The program for 52 weeks lows expect a file in the local dir called "names.txt" with a list of stock symbols to test.

To run simply 

```
python3 -m venv venv

source venv/bin/activate
./main.py
```


