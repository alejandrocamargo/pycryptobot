
import requests
import json
import time

url = 'https://poloniex.com/public?command=returnLoanOrders&currency=BTC'

def get_loans():
    response = requests.get(url)
    json_data = json.loads(response.text)

    demands = json_data["demands"]
    print(type(demands))

    for demand in demands:
        print(demand)


def main():
    while True:
        get_loans()
        time.sleep(10)

main()
