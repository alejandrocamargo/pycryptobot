
import cbpro as cbpro
import time
import datetime
import bot_config
import calcul
import logging
import coinbase
import logger

def main(): 
    logger.configure_logger()
    log = logging.getLogger("Bot")

    btc_prices = []

    auth_client = coinbase.get_auth_client()
    btc_account = coinbase.get_account(auth_client, "BTC")
    eur_account = coinbase.get_account(auth_client, "EUR")

    #log.info(f"Balances: {eur_account['balance']} {eur_account['currency']} | {btc_account['balance']} {btc_account['currency']}")
    log.info("Balances: {} {} | {} {}".format(eur_account['balance'], eur_account['currency'], btc_account['balance'], btc_account['currency']))   

    while True:

        try:

            order = coinbase.get_order(auth_client)

            btc_price = coinbase.get_btc_price()
            btc_prices.append(btc_price)

            btc_avg_price = calcul.average(btc_price, btc_prices)
            btc_mv_avg_price = calcul.moving_average(btc_prices, 20)

            #log.info(f'1 BTC={btc_price} EUR | Avg={btc_avg_price} | Mv. Avg={btc_mv_avg_price}')
            log.info("1 BTC={} EUR | Avg={} | Mv. Avg={}".format(btc_price, btc_avg_price, btc_mv_avg_price))
            
            # give some time to the moving average to make decisions
            if len(btc_prices) > 40:
                make_trading_decision(auth_client, order, btc_price, btc_avg_price, btc_mv_avg_price, eur_account, btc_account)

        except Exception as e:
            #log.error(f"An error has occured: {str(e)}")
            log.error("An error has occured: {}".format(str(e)))
         
        time.sleep(60)

def make_trading_decision(auth_client, order, btc_price, btc_avg_price, btc_mv_avg_price, eur_account, btc_account):
    
    log = logging.getLogger("Bot")

    # We assume no order = buy BTC NOOOOOO
    if order is None:
        log.info("No order placed, evaluating...")

        # Do we have a position > 0.01 BTC ?
        if float(btc_account['balance']) > 0.01:
            # Sell BTC
            if btc_price > btc_avg_price and btc_price > btc_mv_avg_price:
                coinbase.sell_btc_trade(auth_client, btc_price, float(btc_account['balance']))
        else:
            # Buy BTC
            if btc_price < btc_avg_price and btc_price < btc_mv_avg_price:
                coinbase.buy_btc_trade(auth_client, btc_price, float(eur_account['balance']))
            
    else:
        if order['settled'] == False:
            #log.info(f"Order {order['side']}={order['id']} | Price={order['price']} | Status={order['status']} | Seetled={order['settled']}")
            log.info("Order {}={} | Price={} | Status={} | Seetled={}".format(order['side'], order['id'], order['price'], order['status'], order['settled']))

        else:
            # order has been executed
            if order['side'] == "buy":
                # Sell
                if btc_price > btc_avg_price and btc_price > btc_mv_avg_price:
                    coinbase.sell_btc_trade(auth_client, btc_price, float(btc_account['balance']))

            else:
                # Buy
                if btc_price < btc_avg_price and btc_price < btc_mv_avg_price:
                    coinbase.buy_btc_trade(auth_client, btc_price, float(eur_account['balance']))



main()
