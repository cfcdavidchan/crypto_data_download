import os, shutil
from shutil import rmtree
from datetime import date
from open_market_cap import open_market_cap_to_csv
from coinmarketcap import coin_market_cap_to_csv

root = os.getcwd()
#check_directory
if 'csv' not in os.listdir(root):
    os.mkdir('csv')
else:
    pass
csv_path = os.path.join(root, 'csv')
today = str(date.today())
# creating directory for today
if today not in os.listdir(csv_path):
    os.mkdir(os.path.join(csv_path, today))

today_csv_dir = os.path.join(csv_path, today)

# check api file for coinmarketcap
api_path = os.path.join(root, 'coinmarketcap_api.txt')
if not os.path.exists(api_path): #api file not found
    api = input('Please provide your coin market cap api:\n')

    with open(api_path, "w") as text_file: # api text file create
        text_file.write(api)

else:
    with open(api_path, "r") as text_file:
        api = text_file.read()


for i in range(0,100):
    try:
        print('Open market cap data is downloading......')
        open_market_cap_to_csv(csv_dir_path= today_csv_dir)
        print('Finished')
        break
    except:
        print('Open market cap data cannot be downloaded successfully')

for i in range(0,100):
    try:
        print('Coin market cap data is downloading......')
        coin_market_cap_to_csv(api= api, csv_dir_path= today_csv_dir)
        print('Finished')
        break
    except Exception as e:
        print (e)
        print('Coin coin cap data cannot be downloaded successfully')

