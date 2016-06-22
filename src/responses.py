from time import localtime

weekdays = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

help = """Digite /quibe que eu te conto o que as tias do RU estão preparando pra ti hoje

Feito à base sassami de frango empanado

Inspirado em https://voucomerno.ru/ (também é de onde eu pego o cardápio)

Meu repositório: http://github.com/caiopo/quibe-bot"""

_cardapio = """*{weekday}, {day}/{month}*
hoje tem:
- {main}
- {complement}
- {salad}
- {dessert}"""

unknown_command = 'Que isso?'

subscribe = 'Inscrição feita!'

already_subscribed = 'Você já está inscrito!'

unsubscribe = 'Inscrição removida!'

not_subscribed = 'Você não está inscrito!'

def cardapio(menu):
	timenow = localtime()

	return _cardapio.format(
			weekday=weekdays[timenow.tm_wday],
			day=timenow.tm_mday,
			month=timenow.tm_mon,
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
