# app/robo_advisor.py

# TODO: import some modules and/or packages here

# TODO: write some Python code here to produce the desired functionality...

import requests
import json
import datetime

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response = requests.get(request_url)

parsed_response = json.loads(response.text)

run_date = datetime.datetime.now()
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

latest_close = parsed_response["Time Series (Daily)"][last_refreshed]["4. close"]


usd = "${0:,.2f}"

print("-----------------------")
print("STOCK SYMBOL: AMZN")
print("RUN AT: " + run_date.strftime("%Y-%m-%d %I:%M:%S %p")) #adapted from my shopping cart project
print("LATEST DATA FROM: " + last_refreshed)

print("-----------------------")
print("CRUNCHING THE DATA...")

print("-----------------------")
print("LATEST CLOSING PRICE: " + usd.format(float(latest_close)))
print("RECENT HIGH: ")
print("RECENT LOW: ")