import csv, requests, os

def open_market_cap(csv_dir_path):
    csv_file_path = os.path.join(csv_dir_path, 'openmarketcap.csv')

    url = "http://api.openmarketcap.com/api/v1/tokens"
    r = requests.get(url)
    all_data = r.json()['data']

    with open(csv_file_path, mode='w') as csv_file:
        csv_file_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data_key = list(all_data.keys())

        csv_file_writer.writerow(data_key) #write header

        for row in all_data:
            entry = []
            for key in data_key:
                entry.append(row[key])
            csv_file_writer.writerow(entry)

if __name__ == '__main__':

    url = "http://api.openmarketcap.com/api/v1/tokens"
    r = requests.get(url)
    all_data = r.json()

    print(all_data)