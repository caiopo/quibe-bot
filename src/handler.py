import telegram
import config
import responses

from pytz import timezone
from datetime import datetime
from db import Database

# Botfather: /setcommands
# quibe - cardápio do RU
# help - sobre quibebot
# subscribe - inscreve-se para receber o cardápio do RU todos os dias
# unsubscribe - cancela a inscrição


def report_errors(func):
    def catcher(bot, update):
        try:
            func(bot, update)
        except Exception as e:
            error(bot, update, e)
    return catcher


def maintainer_only(func):
    def assert_mntnr(bot, update):
        if str(update.message.chat_id) != config.MAINTAINER_ID:
            return
        func(bot, update)
    return assert_mntnr


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
    if update.message.chat_id > 0:  # user
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=responses.unknown_command)


@report_errors
def quibe(bot, update):
    send_menu(bot, update.message.chat_id)


@report_errors
@maintainer_only
def sendto(bot, update):
    try:
        target = update.message.text.split()[1]
    except IndexError:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='This command needs an argument')
        return

    send_menu(bot, target)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text='Sent')


def error(bot, update, e):
    text = ('Error on @quibebot\nUpdate: {}\n'
            'Error type: {}\nError: {}').format(update, type(e), e)

    bot.sendMessage(chat_id=config.MAINTAINER_ID,
                    text=text)


def send_menu(bot, chat_id, msg=None):
    msg = msg or responses.cardapio()

    if str(chat_id)[0] == '@':  # if channel
        msg = '@quibebot:\n' + msg

    bot.sendMessage(chat_id=chat_id,
                    text=msg,
                    parse_mode=telegram.ParseMode.MARKDOWN)


class AutoMessageManager:
    def __init__(self):
        self.targets = Database()

        self.recently_sent = False

    def subscribe(self, bot, update):
        if self.targets.add(str(update.message.chat_id)):
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=responses.subscribe)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=responses.already_subscribed)

    def unsubscribe(self, bot, update):
        if self.targets.remove(str(update.message.chat_id)):
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=responses.unsubscribe)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text=responses.not_subscribed)

    def job(self, bot):
        try:
            if self.recently_sent:
                self.recently_sent = False
                return

            if valid_time():
                print('preparando para executar o job')

                menu = responses.cardapio()

                self.recently_sent = True

                for chat_id in self.targets:
                    try:
                        send_menu(bot, chat_id, menu)

                    except telegram.error.Unauthorized:
                        self.targets.remove(chat_id)
                        bot.sendMessage(
                            chat_id=config.MAINTAINER_ID,
                            text='Unauthorized: removed {}'.format(chat_id))

                    except telegram.error.ChatMigrated as e:
                        self.targets.remove(chat_id)
                        self.targets.add(str(e.new_chat_id))

                        bot.sendMessage(
                            chat_id=config.MAINTAINER_ID,
                            text='ChatMigrated: {} to {}'.format(
                                chat_id, e.new_chat_id))

                    except Exception as e:
                        error(bot, None, e)

                print('job finalizado')

        except Exception as e:
            error(bot, None, e)


def valid_time():
    now = datetime.now(timezone('America/Sao_Paulo'))

    return (now.hour, now.minute) == config.AUTO_MSG_TIME
