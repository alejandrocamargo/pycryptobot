import cbpro as cbpro
import bot_config
import logging

log = logging.getLogger("Bot")

def get_btc_price():
    public_client = cbpro.PublicClient()
    btc = public_client.get_product_ticker("BTC-EUR")

    for key, value in btc.items():
        if key == "price":
            return float(value)

    # Something went wrong
    raise Exception("Unable to get BTC price")

def get_auth_client():


    return cbpro.AuthenticatedClient(key, b64secret, passphrase)

"""
{'id': '9b944d69-0b9a-4d19-81c5-5dceafba9dd7', 'currency': 'EUR', 'balance': '10.1280360543600000', 'available': '10.12803605436', 'hold': '0.0000000000000000', 'profile_id': '57306844-c41a-4
8ab-91d7-f39117762910'}
"""
def get_account(auth_client, currency):
    
    accounts = auth_client.get_accounts()

    for account in accounts:
        if account['currency'] == currency:
            return account

"""
{'id': '66f12237-1545-4ed6-9987-5e1b217202f8', 'price': '3479.74000000', 'size': '0.02561300', 'product_id': 'BTC-EUR', 'side': 'sell', 'type': 'limit', 'time_in_force': 'GTC', 'post_only': F
alse, 'created_at': '2019-01-10T06:33:22.045906Z', 'fill_fees': '0.0000000000000000', 'filled_size': '0.00000000', 'executed_value': '0.0000000000000000', 'status': 'open', 'settled': False}
"""
def get_order(auth_client):
    
    # returns a generator
    orders = auth_client.get_orders()

    try:
        return next(orders)
    except:
        return None


def buy_btc_trade(auth_client, btc_price, eur_available):

    price = round(btc_price * bot_config.trade_buy_target['target_price'], 2)
    size = round((eur_available * bot_config.trade_buy_target['target_amount']) / price, 8)

    #log.info(f"BUY order -> size: {size} BTC, price: {price} €")
    log.info("BUY order -> size: {} BTC, price: {} EUR".format(size, price))

    order = auth_client.place_limit_order(product_id='BTC-EUR', 
                                        side='buy', 
                                        size=str(size),
                                        price=str(price))

    return order

def sell_btc_trade(auth_client, btc_price, btc_available):

    price = round(btc_price * bot_config.trade_sell_target['target_price'], 2)
    size = round(btc_available * bot_config.trade_sell_target['target_amount'], 8)

    #log.info(f"SELL order -> size: {size} BTC, price: {price} €")
    log.info("SELL order -> size: {} BTC, price: {} EUR".format(size, price))

    order = auth_client.place_limit_order(product_id='BTC-EUR', 
                                        side='sell', 
                                        size=str(size),
                                        price=str(price))

    return order
