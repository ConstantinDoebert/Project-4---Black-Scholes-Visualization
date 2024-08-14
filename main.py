from market.market import *
from options.options import *
from plotter.plotter import *
from portfolio.portfolio import *
from utils.utils import *
from utils.numeric_routines import *

mkt_env = MarketEnvironment()

call = PlainVanillaOption(mkt_env)
call.set_T("15-08-2024")
print(call.price())