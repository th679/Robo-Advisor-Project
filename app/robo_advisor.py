# app/robo_advisor.py

# TODO: import some modules and/or packages here

# TODO: write some Python code here to produce the desired functionality...

import requests
import json

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response = requests.get(request_url)

parsed_response = json.loads(response.text)



print("-----------------------")
print("STOCK SYMBOL: AMZN")

print("-----------------------")
print("CRUNCHING THE DATA...")

print("-----------------------")
print("LATEST CLOSING PRICE: $1,259.19")