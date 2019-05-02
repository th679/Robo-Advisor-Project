from dotenv import load_dotenv
import requests
import json
import datetime
import csv
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import pytest

from app.robo_advisor import to_usd, compile_url, get_response

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
    assert url == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={api_key}"


@pytest.mark.skipif(CI_ENV==True, reason=SKIP_REASON)
def test_get_response():
    parsed_response = get_response("AAPL")
    assert isinstance(parsed_response, dict)
    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == "AAPL"