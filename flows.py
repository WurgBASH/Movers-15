import states
from telegram import (ReplyKeyboardRemove, 
			ReplyKeyboardMarkup, 
			InlineKeyboardMarkup,
			InlineKeyboardButton,
			KeyboardButton, 
			ParseMode)
from telegram.ext import ConversationHandler
from buttons import main_menu, back_menu

from io import BytesIO
from utils import read_table
from db import *

from datetime import datetime


def upload_table_1(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text


	context.bot.send_message(chat_id=chat_id,
		text='Завантажте таблицю в форматі <b>excel</b> <i>(xls, xlsx)</i>',
		parse_mode=ParseMode.HTML,
		reply_markup=back_menu())

	return states.UPLOAD[0]

def upload_table_2(update, context):
	chat_id = update.effective_chat.id

	try:
		buf = BytesIO()
		file_ = context.bot.get_file(update.message.document).download(out=buf)
		file_.seek(0)

		file_data = read_table(file_, context.user_data['data_set'])
		for obj in file_data:
			if context.user_data['data_set'] == 1:
				db.insert_car(obj)
			elif context.user_data['data_set'] == 2:
				db.insert_driver(obj)
			elif context.user_data['data_set'] == 3:
				db.insert_route(obj)

	except Exception as e:
		context.bot.send_message(chat_id=chat_id,
			text='Виникла <b>помилка</b>\nЛог помилки: '+str(e),
			parse_mode=ParseMode.HTML,
			reply_markup=main_menu())
	else:
		context.bot.send_message(chat_id=chat_id,
			text='Данні <b>успішно</b> завантажені',
			parse_mode=ParseMode.HTML,
			reply_markup=main_menu())


	return ConversationHandler.END

def cancel_upload_table(update, context):
	chat_id = update.effective_chat.id
	
	context.bot.send_message(chat_id=chat_id,
			text='Ви в головному меню',
			reply_markup=main_menu())
	return ConversationHandler.END


def add_transportation_1(update, context):
	chat_id = update.effective_chat.id
	context.user_data['transportation'] = {}
	drivers = db.find('drivers')
	if drivers:
		buttons = []
		for driver in drivers:
			buttons.append([InlineKeyboardButton(text=driver[1], callback_data='set_driver$%d'%driver[0])])

		buttons.append([InlineKeyboardButton(text='Завершити вибір', callback_data='save_drivers$')])

		context.bot.send_message(chat_id=chat_id,
		text='Оберіть водіїв:',
		parse_mode=ParseMode.HTML,
		reply_markup=InlineKeyboardMarkup(buttons))

		return states.TRANSPORTATION[0]
	else:
		context.bot.send_message(chat_id=chat_id,
			text='В базі ще немає водіїв',
			reply_markup=main_menu())
		return ConversationHandler.END

def add_transportation_2(update, context):
	chat_id = update.effective_chat.id

	query = update.callback_query

	query.answer()

	wm_command = query.data.split('$')

	if 'drivers' not in context.user_data['transportation']:
		context.user_data['transportation']['drivers'] = []

	if wm_command[0] == 'set_driver':
		driver_id = int(wm_command[1])
		if driver_id not in context.user_data['transportation']['drivers']:
			if len(context.user_data['transportation']['drivers']) < 3:
				context.user_data['transportation']['drivers'].append(driver_id)
			else:
				update.callback_query.message.edit_text('Ліміт 2 водія на одне перевезення')
		else:
			context.user_data['transportation']['drivers'].remove(driver_id)

		buttons = []
		drivers = db.find('drivers')
		for driver in drivers:
			if driver[0] in context.user_data['transportation']['drivers']:
				buttons.append([InlineKeyboardButton(text='✅ '+driver[1], callback_data='set_driver$%d'%driver[0])])
			else:
				buttons.append([InlineKeyboardButton(text=driver[1], callback_data='set_driver$%d'%driver[0])])
		
		buttons.append([InlineKeyboardButton(text='Завершити вибір', callback_data='save_drivers$')])

		update.callback_query.message.edit_text('Оберіть водіїв:')
		update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

		return states.TRANSPORTATION[0]

	elif wm_command[0] == 'save_drivers':
		if len(context.user_data['transportation']['drivers']) >0:
			routes = db.find('routes')

			if routes:
				buttons = []
				for route in routes:
					buttons.append([InlineKeyboardButton(text=route[1], callback_data='set_route$%d'%route[0])])

				buttons.append([InlineKeyboardButton(text='Завершити вибір', callback_data='save_routes$')])

				update.callback_query.message.edit_text('Оберіть маршрут: ')
				update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

				return states.TRANSPORTATION[1]
			else:
				context.bot.send_message(chat_id=chat_id,
					text='В базі ще немає машрутів',
					reply_markup=main_menu())
				return ConversationHandler.END
		else:
			return add_transportation_1(update.callback_query, context)

def add_transportation_3(update, context):
	chat_id = update.effective_chat.id

	query = update.callback_query

	query.answer()

	wm_command = query.data.split('$')

	if 'routes' not in context.user_data['transportation']:
		context.user_data['transportation']['routes'] = []

	if wm_command[0] == 'set_route':
		route_id = int(wm_command[1])
		if route_id not in context.user_data['transportation']['routes']:
			if len(context.user_data['transportation']['routes']) < 2:
				context.user_data['transportation']['routes'].append(route_id)
			else:
				update.callback_query.message.edit_text('Ліміт 1 маршрут на одне перевезення')
		else:
			context.user_data['transportation']['routes'].remove(route_id)

		buttons = []
		routes = db.find('routes')

		for route in routes:
			if route[0] in context.user_data['transportation']['routes']:
				buttons.append([InlineKeyboardButton(text='✅ '+route[1], callback_data='set_route$%d'%route[0])])
			else:
				buttons.append([InlineKeyboardButton(text=route[1], callback_data='set_route$%d'%route[0])])
		
		buttons.append([InlineKeyboardButton(text='Завершити вибір', callback_data='save_routes$')])

		update.callback_query.message.edit_text('Оберіть маршрут')
		update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

		return states.TRANSPORTATION[1]

	elif wm_command[0] == 'save_routes':
		if len(context.user_data['transportation']['routes']) > 0:
			update.callback_query.message.edit_text('Напишіть дату відправлення в форматі дд.мм.рррр')
			return states.TRANSPORTATION[2]
		else:
			routes = db.find('routes')

			if routes:
				buttons = []
				for route in routes:
					buttons.append([InlineKeyboardButton(text=route[1], callback_data='set_route$%d'%route[0])])

				buttons.append([InlineKeyboardButton(text='Завершити вибір', callback_data='save_routes$')])

				update.callback_query.message.edit_text('Оберіть маршрут: ')
				update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

				return states.TRANSPORTATION[1] 


def add_transportation_4(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text

	try:
		date = datetime.strptime(text.replace(' ',''), '%d.%m.%Y')
	except:
		context.bot.send_message(chat_id=chat_id,
			text='Напишіть дату в правильному форматі',
			parse_mode=ParseMode.HTML)
		return states.TRANSPORTATION[2]
	
	context.user_data['transportation']['start_date'] = date

	context.bot.send_message(chat_id=chat_id,
			text='Напишіть дату прибуття в форматі дд.мм.рррр',
			parse_mode=ParseMode.HTML)

	return states.TRANSPORTATION[3]

def add_transportation_5(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text

	try:
		date = datetime.strptime(text.replace(' ',''), '%d.%m.%Y')
	except:
		context.bot.send_message(chat_id=chat_id,
			text='Напишіть дату в правильному форматі',
			parse_mode=ParseMode.HTML)
		return states.TRANSPORTATION[2]

	if date < context.user_data['transportation']['start_date']:
		context.bot.send_message(chat_id=chat_id,
			text='Дата прибуття не може бути раніше ніж дата відправлення\nНапишіть дату прибуття в форматі дд.мм.рррр',
			parse_mode=ParseMode.HTML)
		return states.TRANSPORTATION[3]
	
	context.user_data['transportation']['end_date'] = date
	
	context.bot.send_message(chat_id=chat_id,
			text='Напишіть назву (опис) перевезення',
			parse_mode=ParseMode.HTML)

	return states.TRANSPORTATION[4]

def add_transportation_6(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text

	context.user_data['transportation']['description'] = text

	db.insert_transportation({
		'description':context.user_data['transportation']['description'],
		'route_id': context.user_data['transportation']['routes'][0]
	})

	transportation = db.find_transportation({
		'description':context.user_data['transportation']['description'],
		'route_id': context.user_data['transportation']['routes'][0]
	})
	
	for driver in context.user_data['transportation']['drivers']:
		db.insert_transportation_driver({
			'transportation_id':transportation[0],
			'driver_id': driver
		})

	context.bot.send_message(chat_id=chat_id,
			text='Перевезення успішно збережені',
			reply_markup=main_menu(),
			parse_mode=ParseMode.HTML)

	return ConversationHandler.END

	
def delete_transportations(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text

	# sql = '''SELECT * FROM transportations 
	# JOIN transportation_drivers on transportation_drivers.transportation_id = transportations.transportation_id 
	# JOIN drivers on drivers.driver_id=transportation_drivers.driver_id'''

	# data = db.execute(sql)

	# for info in data:
	# 	print(info)

	transportations = db.find('transportations')
	if transportations:
		for transportation in transportations:
			context.bot.send_message(chat_id=chat_id,
				text=transportation[1],
				reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Видалити', callback_data='delete_transportation$%d'%transportation[0])]]))
	else:
		context.bot.send_message(chat_id=chat_id,
			text='В боті ще немає перевезень',
			reply_markup=main_menu())

	return ConversationHandler.END





