import states
from telegram import (ReplyKeyboardRemove, 
			ReplyKeyboardMarkup, 
			InlineKeyboardMarkup,
			InlineKeyboardButton,
			KeyboardButton, 
			ParseMode)
from telegram.ext import ConversationHandler
from buttons import main_menu
from db import *


def start(update, context):
	chat_id = update.effective_chat.id

	context.bot.send_message(chat_id=chat_id, 
		text='Спочатку вам потрібно зареєструватися в системі',
		parse_mode=ParseMode.HTML)

	context.bot.send_message(chat_id=chat_id, 
		text='Для цього ведіть <b>пароль</b>',
		parse_mode=ParseMode.HTML)

	return states.REGISTRATION[0]

def get_password(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	user = context.bot.get_chat(chat_id)
	
	try:
		db.insert_user({'chat_id':chat_id, 'name':user.first_name})
	except:
		pass

	if text == 'пароль':
		context.bot.send_message(chat_id=chat_id,
			text='Ви в головному меню',
			reply_markup=main_menu(),
			parse_mode=ParseMode.HTML)
		return ConversationHandler.END
	else:
		return start(update, context)

