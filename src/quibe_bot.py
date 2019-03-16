#! /usr/bin/env python3

import logging
import handler
import argparse
import config

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job


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

    dispatcher.add_handler(CommandHandler('start', handler.help))
    dispatcher.add_handler(CommandHandler('help', handler.help))

    dispatcher.add_handler(CommandHandler('quibe', handler.quibe))
    dispatcher.add_handler(CommandHandler('kibe', handler.quibe))

    dispatcher.add_handler(CommandHandler('subscribe', subscribe))
    dispatcher.add_handler(CommandHandler('inscrever', subscribe))

    dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dispatcher.add_handler(CommandHandler('desinscrever', unsubscribe))

    dispatcher.add_handler(MessageHandler(Filters.text, handler.unknown))

    if config.MAINTAINER_ID:
        dispatcher.add_handler(CommandHandler('sendto', handler.sendto))
        dispatcher.add_error_handler(handler.error)

    job_queue.run_repeating(lambda bot, job: auto_msg.job(bot), interval=50)

    updater.start_webhook(
        listen='0.0.0.0', port=config.PORT, url_path=config.BOT_TOKEN)

    updater.bot.set_webhook(config.WEBHOOK_URL)

    updater.idle()
