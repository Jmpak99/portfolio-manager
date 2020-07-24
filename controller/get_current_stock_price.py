import investpy
import json


def get_current_stock_price(stock_symbol, country):
    # param1 = stock ticker symbol, param2 = country name
    current_price_raw = investpy.stocks.get_stock_recent_data(stock_symbol, country, as_json=True, order='descending', interval='Daily')

    current_price_dict = json.loads(current_price_raw)
    # to change dictionary embedded str type to dictionary type

    current_price = current_price_dict['recent'][0]['close']
    # get today's close price for a certain stock

    return current_price
