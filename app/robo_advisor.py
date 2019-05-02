# app/robo_advisor.py

from dotenv import load_dotenv
import requests
import json
import datetime
import csv
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

load_dotenv()

def to_usd(price):
    return "${0:,.2f}".format(price)

def compile_url(symbol, api_key):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    return request_url

def get_response(symbol):
    api_key = os.environ.get("my_API_key")
    url = compile_url(symbol, api_key)
    response = requests.get(url)
    parsed_response = json.loads(response.text)
    if 'Error' in response.text:
        print("Could not find trading data for that stock symbol")
        quit()
        #adapted from https://github.com/hiepnguyen034/robo-stock/blob/master/robo_advisor.py
    return parsed_response

def transform_response(parsed_response):
    tsd = parsed_response["Time Series (Daily)"]
    rows = []
    for date, daily_prices in tsd.items():
        row = {"timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]}
        rows.append(row)
    return rows

def write_to_csv(file_path, rows):
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = csv_headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            #adapted from Project Walkthrough
    return True


symbol = input("Please input a stock symbol: ")

if not symbol.isalpha():
    print("Please enter a proper stock symbol Ex. MSFT")
    quit()

parsed_response = get_response(symbol)

run_date = datetime.datetime.now()
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

data = transform_response(parsed_response)

latest_close = data[0]["close"]


high_prices = []
low_prices = []

for row in data:
    high_price = row["high"]
    high_prices.append(float(high_price))
    low_price = row["low"]
    low_prices.append(float(low_price))

#adapted from Project Walkthrough

recent_high = max(high_prices)

recent_low = min(low_prices)

high_threshold = recent_low * 1.05
medium_threshold = recent_low * 1.10
low_threshold = recent_low * 1.20
low_dontbuy = recent_low * 1.25
medium_dontbuy = recent_low * 1.30


percent_change = (float(latest_close)/recent_low) - 1
above_close = '{:.1%}'.format(percent_change)

if float(latest_close) <= high_threshold:
    decision = "BUY"
    confidence = "HIGH"
    explanation = "The stock's latest closing price is less than 5% above the recent low."
elif float(latest_close) <= medium_threshold:
    decision = "BUY"
    confidence = "MEDIUM"
    explanation = "The stock's latest closing price is 5 to 10% above the recent low."
elif float(latest_close) <= low_threshold:
    decision = "BUY"
    confidence = "LOW"
    explanation = "The stock's latest closing price is 10 to 20% above the recent low."
elif float(latest_close) <= low_dontbuy:
    decision = "DON'T BUY"
    confidence = "LOW"
    explanation = "The stock's latest closing price is 20 to 25% above the recent low."
elif float(latest_close) <= medium_dontbuy:
    decision = "DON'T BUY"
    confidence = "MEDIUM"
    explanation = "The stock's latest closing price is 25 to 30% above the recent low."
else:
    decision = "DON'T BUY"
    confidence = "HIGH"
    explanation = "The stock's latest closing price more than 30% above the recent low."


csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices_" + symbol + ".csv")
write_to_csv(csv_file_path, data)


print("-----------------------")
print("STOCK SYMBOL: " + symbol)
print("RUN AT: " + run_date.strftime("%Y-%m-%d %I:%M:%S %p")) #adapted from my shopping cart project
print("LATEST DATA FROM: " + last_refreshed)

print("-----------------------")
print("CRUNCHING THE DATA...")

print("-----------------------")
print("LATEST CLOSING PRICE: " + to_usd(float(latest_close)))
print("RECENT HIGH: " + to_usd(recent_high))
print("RECENT LOW: " + to_usd(recent_low))
print("-----------------------")

print("RECOMMENDATION: ")
print("DECISION: " + decision)
print("CONFIDENCE LEVEL: " + confidence)
print("EXPLANATION: " + explanation)
print("The closing price is " + above_close + " above the recent low.")
print("-----------------------")


print("WRITING DATA TO CSV: " + csv_file_path)



print("----------------")
print("GENERATING LINE GRAPH...")

closing_prices = []
dates_graph = []

for date in data:
    date = date["timestamp"]
    dates_graph.append(date)

for date in data:
    closing_price = date["close"]
    closing_prices.append(float(closing_price))

fig, ax = plt.subplots()

ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: to_usd(int(x))))
#adapted from https://preinventedwheel.com/matplotlib-thousands-separator-1-step-guide/

ax.xaxis.set_major_locator(plt.MaxNLocator(12))
#adapted from https://jakevdp.github.io/PythonDataScienceHandbook/04.10-customizing-ticks.html 

plt.plot(dates_graph, closing_prices)
plt.xlabel('Day')
plt.ylabel('Closing Price')
plt.title('Closing Stock Prices: ' + symbol)
plt.tight_layout()
plt.show()