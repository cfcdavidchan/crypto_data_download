from requests import Request, Session
import requests, re
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, csv, os
from pprint import pprint
from bs4 import BeautifulSoup
import pandas as pd

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
def top_pair(link, top_number=5):
    target_pair = []

    table_page = requests.get(link)
    soup = BeautifulSoup(table_page.text, 'lxml')
    table = soup.find('tbody')
    all_pair = table.find_all('tr')[0:top_number]
    for pair in all_pair:
        target_pair.append(pair.find('a', {'target': '_blank'}).getText())

    return target_pair

def coinmarket_exchange(target):
    all_exchanges = dict()

    inner_link_start = 'https://coinmarketcap.com'
    exchanges_page = requests.get('https://coinmarketcap.com/rankings/exchanges/')
    soup = BeautifulSoup(exchanges_page.text, 'lxml')
    table = soup.find('tbody')

    all_coins = table.find_all('tr')
    vol_pattern = r'[\d]+'

    for coin in all_coins:
        name = str(coin.find('td', {'class': 'no-wrap currency-name'}).getText()).replace('\n','')
        if name.lower() not in target:
            continue
        inner_link = coin.find('td', {'class': 'no-wrap currency-name'})
        inner_link = inner_link.find(href=True)['href']
        inner_link = inner_link_start + inner_link

        vol = coin.find_all('td',{'class':'no-wrap text-right'})[0].getText()
        vol = ''.join(re.findall(vol_pattern, vol))

        all_exchanges[name] = dict()
        all_exchanges[name]['Adjusted Vol'] = int(vol)
        all_exchanges[name]['Top 5 pair'] = top_pair(inner_link)
    return all_exchanges

def dict_to_pivot_table(dict_data):
    df = pd.DataFrame(dict_data)

    print (df)

if __name__ == '__main__':
    #find api
    # api_path = os.path.join(os.getcwd(), 'coinmarketcap_api.txt')
    # if not os.path.exists(api_path):  # api file not found
    #     api = input('Please provide your coin market cap api:\n')
    #
    #     with open(api_path, "w") as text_file:  # api text file create
    #         text_file.write(api)

    # else:
    #     with open(api_path, "r") as text_file:
    #         api = text_file.read()
    #
    # coin_market_cap_to_csv(api=api, csv_name='test.csv')
    exhange_data = coinmarket_exchange(['huobi','binance','okex','bitmax','kucoin','bitstamp'])

    print (exhange_data)
    dict_to_pivot_table(exhange_data)
    #top_pair('https://coinmarketcap.com/exchanges/bit-z/')












#/v1/cryptocurrency/listings/latest