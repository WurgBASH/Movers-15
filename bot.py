import logging

from base import *
import conversation
import message

import os 

PORT = int(os.environ.get('PORT', '19530'))

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)



def main():
	updater.dispatcher.add_handler(conversation.conv_handler)

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()

