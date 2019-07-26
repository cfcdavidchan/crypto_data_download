import csv, requests, os

def open_market_cap_to_csv(csv_dir_path=os.getcwd(), csv_name='openmarketcap.csv'):
    csv_file_path = os.path.join(csv_dir_path, csv_name)

    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    url = "http://api.openmarketcap.com/api/v1/tokens"
    r = requests.get(url)
    all_data = r.json()['data']

    with open(csv_file_path, mode='w') as csv_file:
        csv_file_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data_key = list(all_data[0].keys())

        csv_file_writer.writerow(data_key) #write header

        for row in all_data:
            entry = []
            for key in data_key:
                entry.append(row[key])
            csv_file_writer.writerow(entry)

if __name__ == '__main__':
    csv_name = 'test.csv'
    open_market_cap_to_csv(csv_name=csv_name)
