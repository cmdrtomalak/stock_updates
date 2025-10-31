import requests
import json
from bs4 import BeautifulSoup


def get_sp_names(url):
    response = requests.get(url)
    symbols = []

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'id': 'constituents'})
    # print(table)

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) > 0:
            ticker_symbol = cells[0].text.strip()
            symbols.append(ticker_symbol)

    # print(len(symbols))
    return symbols


def get_nasdaq_100_symbols(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)

        components_table = None

        components_header = soup.find('h2', {'id': 'Components'})
        # print(components_header)

        if components_header and "Components" in components_header.text:
            components_table = components_header.find_next('table', {'class', 'wikitable'})
            # print(components_table)

        # print(components_table)
        if components_table:
            symbols = []
            for row in components_table.find_all('tr')[1:]:
                cells = row.find_all('td')
                if len(cells) > 0:
                    symbol = cells[1].text.strip()
                    symbols.append(symbol)

            # print(len(symbols))
            return symbols

    return None


def merge_names(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    merged_set = set1.union(set2)

    merged_list = list(merged_set)

    return merged_list


def convert_to_yahoo_symbols(lst):
    converted = [string.replace(".", "-") for string in lst]
    return converted


if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    nasdaq_100_symbols = get_nasdaq_100_symbols(url)

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp_500_symbols = get_sp_names(url)
    # print(sp_500_symbols)

    names = convert_to_yahoo_symbols(merge_names(nasdaq_100_symbols, sp_500_symbols))

    with open('index_names.txt', 'w') as json_file:
        json.dump(names, json_file)

