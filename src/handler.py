import telegram
import config
import time
import responses
import requests
import json
import traceback
from os.path import dirname, realpath

JSON_SOURCE = 'https://voucomerno.ru/menu.json'
AUTO_MSG_PATH = dirname(realpath(__file__)) + '/automsg.txt'
AUTO_MSG_TIME = 11

recently_sent = False

# Botfather: /setcommands
# quibe - cardápio do RU
# help - sobre quibebot
# subscribe - inscreve-se para receber o cardápio do RU todos os dias
# unsubscribe - cancela a inscrição

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
						text=responses.cardapio(resp.json()),
						parse_mode=telegram.ParseMode.MARKDOWN)
	except Exception as e:
		_something_wrong(bot, update, e)

def subscribe(bot, update):
	global automsg_targets

	if update.message.chat_id not in automsg_targets:
		automsg_targets.append(update.message.chat_id)

		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.subscribe)
		_save_automsg()
	else:
		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.already_subscribed)


def unsubscribe(bot, update):
	global automsg_targets

	if update.message.chat_id in automsg_targets:
		automsg_targets.remove(update.message.chat_id)

		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.unsubscribe)
		_save_automsg()
	else:
		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.not_subscribed)


def auto_msg_job(bot):
	global automsg_targets, recently_sent
	timenow = time.localtime()

	resp = requests.get(JSON_SOURCE)

	if recently_sent:
		recently_sent = False
		return

	# sum 1 to correct the time difference between the cloud server and the real UTC-3
	if (timenow.tm_hour + 1) == AUTO_MSG_TIME and timenow.tm_min == 0:
		recently_sent = True
		for chat_id in automsg_targets:
			bot.sendMessage(chat_id=chat_id,
							text=responses.cardapio(resp.json()),
							parse_mode=telegram.ParseMode.MARKDOWN)

def _start_automsg():
	global automsg_targets

	print('Using path:', AUTO_MSG_PATH)

	try:
		with open(AUTO_MSG_PATH) as targets:
			automsg_targets = [int(chat_id.strip('\n')) for chat_id in targets]
	except FileNotFoundError:
		open(AUTO_MSG_PATH, 'w').close()
		automsg_targets = []

def _save_automsg():
	with open(AUTO_MSG_PATH, 'w') as targets:
		for chat_id in automsg_targets:
			targets.write(str(chat_id)+'\n')

def _something_wrong(bot, update, e):
	bot.sendMessage(chat_id=update.message.chat_id,
					text='Something went wrong...\nError type: {}\nError message: {}'.format(type(e), e))

_start_automsg()