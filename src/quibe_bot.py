#! /usr/bin/env python3

import logging
import handler
import argparse
import config

from telegram import Updater


def resolve_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )


if __name__ == '__main__':
    resolve_args()

    updater = Updater(token=config.BOT_TOKEN)

    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    print(updater.bot.getMe())

    auto_msg = handler.AutoMessageManager()

    def subscribe(bot, update):
        auto_msg.subscribe(bot, update)

    def unsubscribe(bot, update):
        auto_msg.unsubscribe(bot, update)

    dispatcher.addTelegramCommandHandler('start', handler.help)
    dispatcher.addTelegramCommandHandler('help', handler.help)

    dispatcher.addTelegramCommandHandler('quibe', handler.quibe)
    dispatcher.addTelegramCommandHandler('kibe', handler.quibe)

    dispatcher.addTelegramCommandHandler('subscribe', subscribe)
    dispatcher.addTelegramCommandHandler('inscrever', subscribe)

    dispatcher.addTelegramCommandHandler('unsubscribe', unsubscribe)
    dispatcher.addTelegramCommandHandler('desinscrever', unsubscribe)

    dispatcher.addTelegramMessageHandler(handler.unknown)
    dispatcher.addUnknownTelegramCommandHandler(handler.unknown)

    if config.MAINTAINER_ID:
        dispatcher.addTelegramCommandHandler('sendto', handler.sendto)
        dispatcher.addErrorHandler(handler.error)

    job_queue.put(lambda bot: auto_msg.job(bot), 50)

    updater.start_webhook(
        listen='0.0.0.0', port=config.PORT, url_path=config.BOT_TOKEN)

    updater.bot.setWebhook(
        'https://' + config.APP_NAME + '.herokuapp.com/' + config.BOT_TOKEN)

    updater.idle()
