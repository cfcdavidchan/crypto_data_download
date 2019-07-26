from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, csv, os
from pprint import pprint

def coin_market_cap_to_csv(api, csv_dir_path=os.getcwd(), csv_name='coinmarketcap.csv', limit = 100, endpoint= '/v1/cryptocurrency/listings/latest', data_key= ['cmc_rank', 'symbol', 'volume_24h', 'price', 'percent_change_24h']):
    csv_file_path = os.path.join(csv_dir_path, csv_name)

    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    url = 'https://pro-api.coinmarketcap.com' + endpoint
    parameters = {
        'start': '1',
        'limit': limit,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api,
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)['data']

    with open(csv_file_path, mode='w') as csv_file:
        csv_file_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file_writer.writerow(data_key)  # write header

        for content in data: #hard coding for the target data#
            row = []
            cmc_rank = content['cmc_rank']
            symbol = content['symbol']
            volume_24h = content['quote']['USD']['volume_24h']
            price = content['quote']['USD']['price']
            percent_change_24h = content['quote']['USD']['percent_change_24h']
            row = [cmc_rank, symbol, volume_24h, price, percent_change_24h]
            csv_file_writer.writerow(row)



if __name__ == '__main__':
    #find api
    api_path = os.path.join(os.getcwd(), 'coinmarketcap_api.txt')
    if not os.path.exists(api_path):  # api file not found
        api = input('Please provide your coin market cap api:\n')

        with open(api_path, "w") as text_file:  # api text file create
            text_file.write(api)

    else:
        with open(api_path, "r") as text_file:
            api = text_file.read()

    coin_market_cap_to_csv(api=api, csv_name='test.csv')












#/v1/cryptocurrency/listings/latest