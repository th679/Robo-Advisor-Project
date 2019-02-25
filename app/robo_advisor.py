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

symbol = input("Please input a stock symbol: ")

if not symbol.isalpha():
    print("Please enter a proper stock symbol Ex. MSFT")
    quit()


api_key = os.environ.get("my_API_key")


request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
response = requests.get(request_url)

if 'Error' in response.text:
    print("Could not find trading data for that stock symbol")
    quit()
    #adapted from https://github.com/hiepnguyen034/robo-stock/blob/master/robo_advisor.py


parsed_response = json.loads(response.text)

run_date = datetime.datetime.now()
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) #adapted from Project Walkthrough https://www.youtube.com/watch?v=UXAVOP1oCog&feature=youtu.be
sorted_dates = sorted(dates, reverse = True)
latest_day = sorted_dates[0]

latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]


high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
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


usd = "${0:,.2f}"


csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices_" + symbol + ".csv")
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
#adapted from Project Walkthrough


print("-----------------------")
print("STOCK SYMBOL: " + symbol)
print("RUN AT: " + run_date.strftime("%Y-%m-%d %I:%M:%S %p")) #adapted from my shopping cart project
print("LATEST DATA FROM: " + last_refreshed)

print("-----------------------")
print("CRUNCHING THE DATA...")

print("-----------------------")
print("LATEST CLOSING PRICE: " + usd.format(float(latest_close)))
print("RECENT HIGH: " + usd.format(recent_high))
print("RECENT LOW: " + usd.format(recent_low))
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
dates_graph = sorted(dates)

for date in dates:
    closing_price = tsd[date]["4. close"]
    closing_prices.append(float(closing_price))

fig, ax = plt.subplots()

ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${0:,.2f}".format(int(x))))
#adapted from https://preinventedwheel.com/matplotlib-thousands-separator-1-step-guide/

ax.xaxis.set_major_locator(plt.MaxNLocator(12))
#adapted from https://jakevdp.github.io/PythonDataScienceHandbook/04.10-customizing-ticks.html 

plt.plot(dates_graph, closing_prices)
plt.xlabel('Day')
plt.ylabel('Closing Price')
plt.title('Closing Stock Prices: ' + symbol)
plt.tight_layout()
plt.show()