import telegram
import config
import time
import responses
import requests
import json

JSON_SOURCE = 'https://voucomerno.ru/menu.json'

# Botfather: /setcommands
# help - sobre quibebot

def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id,
					text=responses.start)

def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id,
					text=responses.help,
					disable_web_page_preview=True)

def unknown(bot, update):
	if update.message.chat_id > 0: # user
		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.unknown_command)

def quibe(bot, update):
	try:
		resp = requests.get(JSON_SOURCE)

		cardapio = json.loads(resp.text)

		resposta = ('hoje tem\n'
					'{main}\n'
					'{complement} pra complementar\n'
					'vai ter {salad} de salada\n'
					'e de sobremesa tem {dessert}').format(
					main=cardapio['main'],
					complement=cardapio['complement'],
					salad=cardapio['salad'],
					dessert=cardapio['dessert'])

		bot.sendMessage(chat_id=update.message.chat_id,
						text=resposta)
	except Exception as e:
		_something_wrong(bot, update, e)

def _something_wrong(bot, update, e):
	bot.sendMessage(chat_id=update.message.chat_id,
					text='Something went wrong...\nError type: {}\nError message: {}'.format(type(e), e))
