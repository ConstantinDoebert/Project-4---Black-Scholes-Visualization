from market.market import *
from options.options import *
from plotter.plotter import *
from portfolio.portfolio import *
import requests as rq
import pandas as pd
from json import load
from datetime import datetime


with open('keys.json') as f:
    key_twelvedata = load(f)["keys"]["twelvedata"]
    key_alphavantage = load(f)["keys"]["alphavantage"]




def get_ecb_rates():
    '''
    Docs: https://data.ecb.europa.eu/help/api/overview
    Data directory: https://data.ecb.europa.eu/data/datasets
    '''
    entrypoint = 'https://data-api.ecb.europa.eu/service/'
    resource = 'data'           # The resource for data queries is always'data'. Do not change.
    flowRef ='FM'              # Repsonsible agency for maintaining data freed
    key = 'D.U2.EUR.4F.KR.DFR.LEV' # https://data.ecb.europa.eu/data/datasets/FM/FM.D.U2.EUR.4F.KR.DFR.LEV
        
    
    parameters = {
        'startPeriod': dt.datetime.strftime(dt.datetime.today(), "%Y-%m-%d"),
        'format': 'jsondata'
    }

    request_url = entrypoint + resource + '/'+ flowRef + '/' + key

    response = get(request_url, params=parameters).json()
    deposit_facility = response["dataSets"][0]["series"]["0:0:0:0:0:0:0"]["observations"]["0"][0] / 100

    return deposit_facility



def calculate_iv(*args, **kwargs):

    _, ticker = initiate_mkt_env()

    options = rq.get(f"https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={ticker}&apikey={key_alphavantage}").json()
    



def initiate_mkt_env(*args, **kwargs):

    ticker = args[0] if len(args) > 0 \
                else kwargs["ticker"] if "ticker" in kwargs \
                else "NVDA"
    
    price_cache = {}
    price = rq.get(f"https://api.twelvedata.com/price?symbol={ticker}&apikey={key_twelvedata}")
    price_cache["price"] = float(price.json()["price"])
    price_cache["t"] = datetime.now()
    
    r = get_ecb_rates()

    mkt_env = MarketEnvironment(S_t=price_cache["price"], t=price_cache["t"], r=r)

    return mkt_env, ticker
    


def plot_single_tau():
    mkt_env, _ = initiate_mkt_env()
    call = PlainVanillaOption(mkt_env)

    option_plotter = OptionPlotter(call)
    
    emission_date = call.get_t()
    expiration_date = call.get_T()
    almost_expiration_date = expiration_date - dt.timedelta(days=10)
    multiple_datetime_valuation_dates = pd.date_range(start=emission_date, end=almost_expiration_date, periods=5)
    
    option_plotter.plot(t=multiple_datetime_valuation_dates, plot_details=True, plot_metrics="PnL")


plot_single_tau()