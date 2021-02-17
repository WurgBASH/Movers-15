from buttons import main_menu, settings_menu, transported_menu, reports_menu, documents_menu
from telegram.ext import ConversationHandler
import flows
from db import *

def handle(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text

	#Меню
	if text == 'Редагувати перевезення':
		context.bot.send_message(chat_id=chat_id,
			text='Оберіть пункт меню',
			reply_markup=transported_menu())
	elif text == 'Завантаження звітів':
		context.bot.send_message(chat_id=chat_id,
			text='Оберіть пункт меню',
			reply_markup=reports_menu())
	elif text == 'Завантаження документів':
		context.bot.send_message(chat_id=chat_id,
			text='Оберіть пункт меню',
			reply_markup=documents_menu())
	elif text == 'Налаштування':
		context.bot.send_message(chat_id=chat_id,
			text='Ви в налаштуваннях',
			reply_markup=settings_menu())
	elif text == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви в головному меню',
			reply_markup=main_menu())
	
	#Функционал
	elif text == 'Завантажити машини':
		context.user_data['data_set'] = 1
		return flows.upload_table_1(update, context)
	elif text == 'Завантажити водіїв':
		context.user_data['data_set'] = 2
		return flows.upload_table_1(update, context)
	elif text == 'Завантажити маршрути':
		context.user_data['data_set'] = 3
		return flows.upload_table_1(update, context)

	elif text == 'Додати перевезення':
		return flows.add_transportation_1(update, context)
	elif text == 'Видалити перевезення':
		return flows.delete_transportations(update, context)
	
	return ConversationHandler.END




def callback(update, context):
	query = update.callback_query

	query.answer()
	wm_command = query.data.split('$')

	if wm_command[0] == 'delete_transportation':
		transportation_id = int(wm_command[1])
		try:
			test = db.execute('DELETE FROM transportations WHERE transportation_id = %d;'%transportation_id)
		except:
			update.callback_query.message.edit_text('Виникла помилка')
		else:
			update.callback_query.message.edit_text('Успішно видален')

	return ConversationHandler.END








