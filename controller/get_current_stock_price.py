import investpy
import json


# get parameters (stock ticker symbol, country name)
def get_current_stock_price(stock_symbol, country):
    current_price_raw = investpy.stocks.get_stock_recent_data(stock_symbol, country, as_json=True, order='descending', interval='Daily')

    # to change dictionary embedded str type to dictionary type
    current_price_dict = json.loads(current_price_raw)

    # get today's close price for a certain stock
    current_price = current_price_dict['recent'][0]['close']


    return current_price
