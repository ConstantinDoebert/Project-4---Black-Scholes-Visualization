from market.market import *
from options.options import *
from plotter.plotter import *
from portfolio.portfolio import *
import requests as rq
import pandas as pd
from json import load
from datetime import datetime
import io


with open('key.json') as f:
    key = load(f)["key"]


def initiate_mkt_env(*args, **kwargs):

    ticker = args[0] if len(args) > 0 \
                else kwargs["ticker"] if "ticker" in kwargs \
                else "NVDA"
    
    price_cache = {}
    price = rq.get(f"https://api.twelvedata.com/price?symbol={ticker}&apikey={key}")
    price_cache["price"] = float(price.json()["price"])
    price_cache["t"] = datetime.now()
    
    mkt_env = MarketEnvironment(S_t=price_cache["price"], t=price_cache["t"])

    return mkt_env
    
def plot_single_tau():
    mkt_env = initiate_mkt_env()
    call = PlainVanillaOption(mkt_env)

    option_plotter = OptionPlotter(call)
    
    emission_date = call.get_t()
    expiration_date = call.get_T()
    almost_expiration_date = expiration_date - dt.timedelta(days=10)
    multiple_datetime_valuation_dates = pd.date_range(start=emission_date, end=almost_expiration_date, periods=5)
    
    option_plotter.plot(t=multiple_datetime_valuation_dates, plot_details=True, plot_metrics="PnL")

plot_single_tau()