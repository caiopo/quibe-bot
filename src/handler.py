import telegram
import config
import time
import responses
import requests
import json
from os.path import dirname, realpath

JSON_SOURCE = 'https://voucomerno.ru/menu.json'
AUTOMSG_PATH = dirname(realpath(__file__)) + '/automsg.txt'

# Botfather: /setcommands
# quibe - cardápio do RU
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

		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.cardapio(resp.json()))
	except Exception as e:
		_something_wrong(bot, update, e)

def subscribe(bot, update):
	global automsg_targets

	if update.message.chat_id not in automsg_targets:
		automsg_targets.append(update.message.chat_id)
		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.subscribe)
	else:
		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.already_subscribed)
	_save_automsg()


def unsubscribe(bot, update):
	global automsg_targets

	if update.message.chat_id in automsg_targets:
		automsg_targets.remove(update.message.chat_id)

		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.unsubscribe)
	else:
		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.not_subscribed)


def auto_msg_job(bot):
	timenow = time.localtime()

	# sum 2 to correct the time difference between the cloud server and the real UTC-3
	if (timenow.tm_hour + 2) in AUTO_MSG_TIME and timenow.tm_min == 0:
		for chat_id in auto_msg_targets:
			try:

			except Exception as e:
				traceback.print_exc()

def _start_automsg():
	global automsg_targets
	try:
		with open('automsg.txt') as targets:
			automsg_targets = [int(chat_id.strip('\n')) for chat_id in targets]
	except FileNotFoundError:
		open('automsg.txt', 'w').close()
		automsg_targets = []

def _save_automsg():
	with open('automsg.txt', 'w') as targets:
		for chat_id in auto_msg_targets:
			targets.write(str(chat_id)+'\n')

def _something_wrong(bot, update, e):
	bot.sendMessage(chat_id=update.message.chat_id,
					text='Something went wrong...\nError type: {}\nError message: {}'.format(type(e), e))
