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
		logging.basicConfig(level=logging.DEBUG,
							format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
	resolve_args()

	updater = Updater(token=config.BOT_TOKEN)

	dispatcher = updater.dispatcher
	job_queue = updater.job_queue

	print(updater.bot.getMe())

	dispatcher.addTelegramCommandHandler('start', handler.help)
	dispatcher.addTelegramCommandHandler('help', handler.help)

	dispatcher.addTelegramCommandHandler('quibe', handler.quibe)
	dispatcher.addTelegramCommandHandler('kibe', handler.quibe)

	dispatcher.addTelegramCommandHandler('subscribe', handler.subscribe)
	dispatcher.addTelegramCommandHandler('inscrever', handler.subscribe)

	dispatcher.addTelegramCommandHandler('unsubscribe', handler.unsubscribe)
	dispatcher.addTelegramCommandHandler('desinscrever', handler.unsubscribe)


	dispatcher.addTelegramMessageHandler(handler.unknown)
	dispatcher.addUnknownTelegramCommandHandler(handler.unknown)

	if config.MAINTAINER_ID:
		dispatcher.addTelegramCommandHandler('sendto', handler.sendto)
		dispatcher.addErrorHandler(handler.error)

	job_queue.put(handler.auto_msg_job, 50)

	updater.start_polling()

if __name__ == '__main__':
	main()