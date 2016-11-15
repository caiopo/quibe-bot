import requests
import bs4

from datetime import datetime
from pprint import pprint

def fetch():
    resp = requests.get('http://ru.ufsc.br/ru/')

    if not resp.ok:
        return []

    bs = bs4.BeautifulSoup(resp.content, 'html.parser')

    cardapio = [entry.text for entry in bs.find_all(align='center')][3:]

    weekday = datetime.now().weekday()

    today = cardapio[(weekday * 6 + 2):(weekday * 6 + 6)]

    today = [item.strip(' \n\xa0').replace('\n', '').lower() for item in today]

    return today


if __name__ == '__main__':
    import responses

    print(responses.cardapio())