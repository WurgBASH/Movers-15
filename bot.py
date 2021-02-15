import logging

from base import *
import conversation

from telegram.ext import (
	MessageHandler,
	Filters,
)

import os 

PORT = int(os.environ.get('PORT', '19530'))

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def handle_all(update, context):
	print('Пришло сообщение от пользователя...')

def main():
	updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_all))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()

