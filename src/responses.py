from pytz import timezone
from datetime import datetime

weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

help = """Digite /quibe que eu te conto o que as tias do RU estão preparando pra ti hoje

Você também pode me enviar /subscribe e eu te enviarei o cardápio do RU todos os dias

Inspirado em https://voucomerno.ru/ (também é de onde eu pego o cardápio)

Meu repositório: http://github.com/caiopo/quibe-bot

Feito por @caiopo"""

_cardapio = """*{weekday}, {day}/{month}*
hoje tem:
\u2022 {main}
\u2022 {complement}
\u2022 {salad}
\u2022 {dessert}"""

unknown_command = 'Que isso?'

subscribe = 'Inscrição feita!'

already_subscribed = 'Você já está inscrito!'

unsubscribe = 'Inscrição removida!'

not_subscribed = 'Você não está inscrito!'

def cardapio(menu):
	timetuple = datetime.now(timezone('America/Sao_Paulo')).timetuple()

	return _cardapio.format(
			weekday=weekdays[timetuple.tm_wday],
			day=timetuple.tm_mday,
			month=str(timetuple.tm_mon).zfill(2),
			main=menu['main'],
			complement=menu['complement'],
			salad=menu['salad'],
			dessert=menu['dessert'])

if __name__ == '__main__':
	import json
	import requests
	from handler import JSON_SOURCE

	resp = requests.get(JSON_SOURCE)

	menu = json.loads(resp.text)

	timenow = time.localtime()

	print(cardapio(menu, timenow))
