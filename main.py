
import numpy as np 
import cbpro as cbpro
import time as time
import pandas as pd
import matplotlib.pyplot as p



def get_btc_price():
    public_client = cbpro.PublicClient()
    btc = public_client.get_product_ticker("BTC-EUR")

    for key, value in btc.items():
        if key == "price":
            return value

def get_btc_average_price(btc_price, btc_prices):
    btc_prices.append(btc_price)
    btc_array = np.array(btc_prices)
    return np.mean(btc_array)
    
def get_btc_moving_average_price(btc_prices):
    df = pd.DataFrame(btc_prices, columns=['prices'])
    ma = df.rolling(5).mean()
    return ma.tail()

def movingaverage(values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma[-1]

def main():

    btc_prices = []

    while True:
        btc_price = float(get_btc_price())
        btc_prices.append(btc_price)
        btc_price_avg = get_btc_average_price(btc_price, btc_prices)
        btc_mv_avg = movingaverage(btc_prices, 10)

        print(f'BTC: {btc_price} -- Avg: {btc_price_avg} -- Mv. Avg: {btc_mv_avg}')
        time.sleep(1)


main()

