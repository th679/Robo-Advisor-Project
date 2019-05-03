from dotenv import load_dotenv
import requests
import json
import datetime
import csv
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import pytest

from app.robo_advisor import to_usd, compile_url, get_response, transform_response, write_to_csv

def test_to_usd():
    assert to_usd(5) == "$5.00"
    assert to_usd(5.777) == "$5.78"
    assert to_usd(12345) == "$12,345.00"

load_dotenv()
api_key = os.environ.get("my_API_key")

CI_ENV = os.environ.get("CI") == "true"
SKIP_REASON = "to avoid issuing requests from the CI server"

def test_compile_url():
    url = compile_url("AAPL", api_key)
    assert url == f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={api_key}"


@pytest.mark.skipif(CI_ENV==True, reason=SKIP_REASON)
def test_get_response():
    parsed_response = get_response("AAPL")
    assert isinstance(parsed_response, dict)
    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == "AAPL"

def test_transform_response():
    parsed_response = {
    "Meta Data": {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": "AAPL",
        "3. Last Refreshed": "2019-05-02 16:00:01",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
        },
    "Time Series (Daily)": {
        "2019-05-02": {
            "1. open": "209.8400",
            "2. high": "212.6500",
            "3. low": "208.1300",
            "4. close": "209.1500",
            "5. volume": "29368219"
            },
        "2019-05-01": {
            "1. open": "209.8800",
            "2. high": "215.3100",
            "3. low": "209.2300",
            "4. close": "210.5200",
            "5. volume": "63420533"
            }
        }
    }
    transformed_response = transform_response(parsed_response)
    expected_response = [
        {'timestamp': '2019-05-02', 'open': '209.8400', 'high': '212.6500', 'low': '208.1300', 'close': '209.1500', 'volume': '29368219'},
        {'timestamp': '2019-05-01', 'open': '209.8800', 'high': '215.3100', 'low': '209.2300', 'close': '210.5200', 'volume': '63420533'}
    ]
    assert transformed_response == expected_response


def test_write_csv():
    example_data = [
        {'timestamp': '2019-05-02', 'open': '209.8400', 'high': '212.6500', 'low': '208.1300', 'close': '209.1500', 'volume': '29368219'},
        {'timestamp': '2019-05-01', 'open': '209.8800', 'high': '215.3100', 'low': '209.2300', 'close': '210.5200', 'volume': '63420533'},
        {'timestamp': '2019-04-30', 'open': '203.0600', 'high': '203.4000', 'low': '199.1100', 'close': '200.6700', 'volume': '46534923'},
        {'timestamp': '2019-04-29', 'open': '204.4000', 'high': '205.9700', 'low': '203.8600', 'close': '204.6100', 'volume': '22204716'}
    ]
    csv_file_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample.csv")
    result = write_to_csv(csv_file_path, example_data)
    assert result == True
    assert os.path.isfile(csv_file_path) == True
