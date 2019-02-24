# app/robo_advisor.py

# TODO: import some modules and/or packages here

# TODO: write some Python code here to produce the desired functionality...

import requests
import json
import datetime
import csv
import os

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response = requests.get(request_url)

parsed_response = json.loads(response.text)

run_date = datetime.datetime.now()
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) #adapted from Project Walkthrough https://www.youtube.com/watch?v=UXAVOP1oCog&feature=youtu.be
sorted_dates = sorted(dates, reverse = True)
latest_day = sorted_dates[0]

latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]

high_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
#adapted from Project Walkthrough

recent_high = max(high_prices)


low_prices = []

for date in dates:
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_low = min(low_prices)

usd = "${0:,.2f}"

print("-----------------------")
print("STOCK SYMBOL: AMZN")
print("RUN AT: " + run_date.strftime("%Y-%m-%d %I:%M:%S %p")) #adapted from my shopping cart project
print("LATEST DATA FROM: " + last_refreshed)

print("-----------------------")
print("CRUNCHING THE DATA...")

print("-----------------------")
print("LATEST CLOSING PRICE: " + usd.format(float(latest_close)))
print("RECENT HIGH: " + usd.format(recent_high))
print("RECENT LOW: " + usd.format(recent_low))

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
print("WRITING DATA TO CSV: " + csv_file_path)

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = csv_headers)
    writer.writeheader()
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

