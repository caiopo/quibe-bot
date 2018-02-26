import requests
import bs4

from pytz import timezone
from datetime import datetime


def fetch():
    resp = requests.get('http://ru.ufsc.br/ru/')

    if not resp.ok:
        return []

    soup = bs4.BeautifulSoup(resp.content, 'lxml')
    table = soup.find('div', class_='content clearfix').find('table')

    rows = table.find_all('tr')
    weekday = datetime.now(timezone('America/Sao_Paulo')).weekday()

    today = [entry.get_text(strip=True)
             for entry in rows[weekday].find_all('td')[1:]]

    return today
