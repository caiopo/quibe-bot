import telegram
import config
import responses
import requests
import traceback

from pytz import timezone
from datetime import datetime
from os.path import dirname, realpath

# Botfather: /setcommands
# quibe - cardápio do RU
# help - sobre quibebot
# subscribe - inscreve-se para receber o cardápio do RU todos os dias
# unsubscribe - cancela a inscrição

JSON_SOURCE = 'https://voucomerno.ru/menu.json'
AUTO_MSG_PATH = dirname(realpath(__file__)) + '/automsg.txt'
AUTO_MSG_TIME = (10, 40)

recently_sent = False

def report_errors(func):
	def catcher(bot, update):
		try:
			func(bot, update)
		except Exception as e:
			error(bot, update, e)
	return catcher


@report_errors
def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id,
					text=responses.start)

@report_errors
def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id,
					text=responses.help,
					disable_web_page_preview=True)

@report_errors
def unknown(bot, update):
	if update.message.chat_id > 0: # user
		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.unknown_command)

@report_errors
def quibe(bot, update):
	_send_menu(bot, update.message.chat_id)

@report_errors
def subscribe(bot, update):
	global automsg_targets

	if str(update.message.chat_id) not in automsg_targets:
		automsg_targets.append(str(update.message.chat_id))

		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.subscribe)
		_save_automsg()
	else:
		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.already_subscribed)

@report_errors
def unsubscribe(bot, update):
	global automsg_targets

	if str(update.message.chat_id) in automsg_targets:
		automsg_targets.remove(str(update.message.chat_id))

		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.unsubscribe)
		_save_automsg()
	else:
		bot.sendMessage(chat_id=update.message.chat_id,
						text=responses.not_subscribed)

@report_errors
def sendto(bot, update):
	if str(update.message.chat_id) != config.MAINTAINER_ID:
		bot.sendMessage(chat_id=update.message.chat_id,
						text='This feature is only enabled to the maintainer')
		return

	try:
		target = update.message.text.split()[1]
	except IndexError:
		bot.sendMessage(chat_id=update.message.chat_id,
						text='This command needs an argument')
		return

	resp = requests.get(JSON_SOURCE)

	_send_menu(bot, target, resp.json())

def error(bot, update, e):
	bot.sendMessage(chat_id=config.MAINTAINER_ID,
					text='Error on @quibebot\nUpdate: {}\nError type: {}\nError: {}'.format(update, type(e), e))

def auto_msg_job(bot):
	try:
		global automsg_targets, recently_sent

		if recently_sent:
			recently_sent = False
			return

		if _valid_time():
			menu_dict = requests.get(JSON_SOURCE).json()

			recently_sent = True

			for chat_id in automsg_targets:
				_send_menu(bot, chat_id, menu_dict)
	except Exception as e:
		error(bot, None, e)

def _send_menu(bot, chat_id, menu_dict=None):
	if not menu_dict:
		menu_dict = requests.get(JSON_SOURCE).json()

	msg = responses.cardapio(menu_dict)

	if str(chat_id)[0] == '@':
		msg = '@quibebot:\n' + msg

	bot.sendMessage(chat_id=chat_id,
					text=msg,
					parse_mode=telegram.ParseMode.MARKDOWN)

def _start_automsg():
	global automsg_targets

	print('Using file:', AUTO_MSG_PATH)

	try:
		with open(AUTO_MSG_PATH) as targets:
			automsg_targets = [chat_id.strip('\n') for chat_id in targets]
	except FileNotFoundError:
		open(AUTO_MSG_PATH, 'w').close()
		automsg_targets = []

	print(automsg_targets)

def _save_automsg():
	global automsg_targets
	with open(AUTO_MSG_PATH, 'w') as targets:
		for chat_id in automsg_targets:
			targets.write(chat_id+'\n')

	print(automsg_targets)


def _valid_time():
	timetuple = datetime.now(timezone('America/Sao_Paulo')).timetuple()

	return (timetuple.tm_hour, timetuple.tm_min) == AUTO_MSG_TIME

_start_automsg()
