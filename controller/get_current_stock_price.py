import investpy
import json
import re


# get parameter (stock ticker symbol), and decide whether the country is south korea or united states
def get_current_stock_price(stock_symbol):
    # south korea ticker symbol starts with a number while that of United states starts with an alphabet
    x = re.search("[0-9]", stock_symbol)

    if x:
        country = "south korea"

    else:
        country = "united States"


    current_price_raw = investpy.stocks.get_stock_recent_data(stock_symbol, country, as_json=True, order='descending', interval='Daily')

    # to change dictionary embedded str type to dictionary type
    current_price_dict = json.loads(current_price_raw)

    # get today's close price for a certain stock
    current_price = current_price_dict['recent'][0]['close']


    return current_price