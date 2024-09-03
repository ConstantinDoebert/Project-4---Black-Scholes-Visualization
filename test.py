from json import load
from requests import get
import datetime as dt


with open('keys.json') as f:
    file = load(f)
    key_twelvedata = file["keys"]["twelvedata"]
    key_alphavantage = file["keys"]["alphavantage"]


options = get(f"https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=NVDA&apikey={key_alphavantage}").json()
