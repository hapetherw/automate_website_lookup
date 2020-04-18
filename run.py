import pandas as pd
import requests


def main():
    url = 'https://bulkdacheck.com/getdata.php'
    file = open('Example Website List.txt', 'r+')
    website_list = file.readlines()
    data_list = []
    data_list = pd.read_csv('result.csv').values.tolist()
    old_site_list = pd.read_csv('result.csv', usecols=['Site Name']).values.tolist()
    count = len(data_list) if data_list is not None else 0
    for index, site in enumerate(website_list):
        response = requests.get(url, {'url': site.strip('\n')}).json()
        try:
            update_idx = old_site_list.index([response['url']])
            old_number = data_list[update_idx][0]
            new = (old_number, response['url'], response['da'], response['pa'], response['mozrank'], response['a_rank'],
                   response['tf'],
                   response['cf'], response['sr_traffic'], response['ip'])
            data_list[update_idx] = new
            print("update" + str(old_number), new)
        except ValueError:
            new = (count + 1, response['url'], response['da'], response['pa'], response['mozrank'], response['a_rank'],
                   response['tf'],
                   response['cf'], response['sr_traffic'], response['ip'])
            data_list.append(new)
            count = count + 1
            print("insert" + str(new[0]), new)
        if (index + 1) % 100 == 0:
            print("saved")
            df = pd.DataFrame(data_list,
                              columns=['#', 'Site Name', 'DA', 'PA', 'Moz Rank', 'Alexa Rank', 'CF', 'TF',
                                       'Semrush Traffic',
                                       'IP'])
            df.to_csv('result.csv', index=False)
    df = pd.DataFrame(data_list,
                      columns=['#', 'Site Name', 'DA', 'PA', 'Moz Rank', 'Alexa Rank', 'CF', 'TF',
                               'Semrush Traffic',
                               'IP'])
    df.to_csv('result.csv', index=False)


print("Start work")
print("------------------------------------------")
if __name__ == "__main__":
    main()

print("------------------------------------------")
print("Finished work")
