import os, shutil
from shutil import rmtree
from datetime import date

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
else:
    rmtree(os.path.join(csv_path, today))
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

