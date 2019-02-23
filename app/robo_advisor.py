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



print("-----------------------")
print("STOCK SYMBOL: AMZN")
print("RUN AT: " + run_date.strftime("%Y-%m-%d %I:%M:%S %p"))
print("LATEST DATA FROM: " + last_refreshed)

print("-----------------------")
print("CRUNCHING THE DATA...")

print("-----------------------")
print("LATEST CLOSING PRICE: $1,259.19")
print("RECENT HIGH: ")
print("RECENT LOW: ")