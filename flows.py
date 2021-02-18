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
from utils import read_table, write_table
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
			if len(context.user_data['transportation']['routes']) < 1:
				context.user_data['transportation']['routes'].append(route_id)
				update.callback_query.message.edit_text('Оберіть маршрут')
			else:
				update.callback_query.message.edit_text('Ліміт 1 маршрут на одне перевезення')
		else:
			context.user_data['transportation']['routes'].remove(route_id)
			update.callback_query.message.edit_text('Оберіть маршрут')

		buttons = []
		routes = db.find('routes')

		for route in routes:
			if route[0] in context.user_data['transportation']['routes']:
				buttons.append([InlineKeyboardButton(text='✅ '+route[1], callback_data='set_route$%d'%route[0])])
			else:
				buttons.append([InlineKeyboardButton(text=route[1], callback_data='set_route$%d'%route[0])])
		
		buttons.append([InlineKeyboardButton(text='Завершити вибір', callback_data='save_routes$')])

		
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
		'route_id': context.user_data['transportation']['routes'][0],
		'start_date': context.user_data['transportation']['start_date'], 
		'end_date': context.user_data['transportation']['end_date']
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



def griver_payments(update, context):
	chat_id = update.effective_chat.id

	sql = '''
	SELECT drivers.name, drivers.experience, SUM(routes.distance), SUM(routes.payment) FROM transportations 
	JOIN transportation_drivers 
	on transportation_drivers.transportation_id = transportations.transportation_id
	JOIN drivers
	on drivers.driver_id = transportation_drivers.driver_id
	JOIN routes
	on routes.route_id = transportations.route_id
	'''
	data = []
	payments = db.execute(sql)
	for payment in payments:
		premia = payment[1] * payment[2] * 0.01
		data.append((payment[0], payment[3], premia, 'Весь'))


	table, tablename = write_table(1, data)
	table.seek(0)
	context.bot.send_message(chat_id=chat_id,
		text='Відомість успішно сформована')

	context.bot.send_document(chat_id=chat_id,
		document=table,
		filename=tablename,
		reply_markup=main_menu())

	return ConversationHandler.END

def transportation_payments(update, context):
	chat_id = update.effective_chat.id

	sql = '''
	SELECT routes.name, drivers.name, drivers.experience, transportations.start_date, transportations.end_date, routes.payment, routes.distance 
	FROM transportations
	join transportation_drivers on transportation_drivers.transportation_id = transportations.transportation_id
	join drivers on transportation_drivers.driver_id = drivers.driver_id
	Join routes On transportations.route_id = routes.route_id
	'''
	data = []
	payments = db.execute(sql)
	for payment in payments:
		premia = payment[2] * payment[6] * 0.01
		sum_ =  premia+payment[5]
		data.append((payment[0], payment[1], payment[3].split(' ')[0], payment[4].split(' ')[0], sum_))


	table, tablename = write_table(2, data)
	table.seek(0)
	context.bot.send_message(chat_id=chat_id,
		text='Відомість успішно сформована')

	context.bot.send_document(chat_id=chat_id,
		document=table,
		filename=tablename,
		reply_markup=main_menu())

	return ConversationHandler.END


def change_tarif(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text

	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END

	if 'change_id' in context.user_data:
		#Идем дальше
		fuels = db.find('fuels')
		try:
			float(text)
		except:
			data = fuels[context.user_data['change_id']]
			context.bot.send_message(chat_id=chat_id,
				text='Введіть ціну за %s'%data[1],
				reply_markup=back_menu())

			return states.TARIF[0]
		else:
			price = float(text)
			sql='''
			UPDATE fuels
			SET price = '''+text+'''
			WHERE fuel_id = '''+str(context.user_data['change_id'])+''';
			'''
			db.execute(sql)
			context.user_data['change_id'] +=1
			if context.user_data['change_id'] < len(fuels):
				data = fuels[context.user_data['change_id']]
				context.bot.send_message(chat_id=chat_id,
				text='Введіть ціну за %s'%data[1],
				reply_markup=back_menu())

				return states.TARIF[0]
			else:
				context.bot.send_message(chat_id=chat_id,
					text='Тарифи успішно збережені',
					reply_markup=main_menu())
				return ConversationHandler.END

	else:
		fuels = db.find('fuels')
		context.user_data['change_id'] = 1
		data = fuels[context.user_data['change_id']]
		context.bot.send_message(chat_id=chat_id,
			text='Введіть ціну за %s'%data[1],
			reply_markup=back_menu())

		return states.TARIF[0]



def get_all_drivers(update, context):
	chat_id = update.effective_chat.id

	drivers = db.find('drivers')
	if drivers:
		context.bot.send_message(chat_id=chat_id,
			text='<b>Редагування водіїв</b>', parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardMarkup([['Додати водія'], ['Повернутися в меню']], resize_keyboard=True))

		for driver in drivers:
			context.bot.send_message(chat_id=chat_id,
				text=driver[1],
				reply_markup=InlineKeyboardMarkup([
					[InlineKeyboardButton('Видалити', callback_data='delete_driver$'+str(driver[0]))]
					]))
	else:
		context.bot.send_message(chat_id=chat_id,
			text='В боті ще немає водіїв',
			reply_markup=main_menu())


	return ConversationHandler.END

def get_all_routes(update, context):
	chat_id = update.effective_chat.id

	routes = db.find('routes')
	if routes:
		context.bot.send_message(chat_id=chat_id,
			text='<b>Редагування маршрутів</b>', parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardMarkup([['Додати маршрут'], ['Повернутися в меню']], resize_keyboard=True))

		for route in routes:
			context.bot.send_message(chat_id=chat_id,
				text=route[1],
				reply_markup=InlineKeyboardMarkup([
					[InlineKeyboardButton('Видалити', callback_data='delete_route$'+str(route[0]))]
					]))
	else:
		context.bot.send_message(chat_id=chat_id,
			text='В боті ще немає маршрутів',
			reply_markup=main_menu())


	return ConversationHandler.END

def get_all_cars(update, context):
	chat_id = update.effective_chat.id

	cars = db.find('cars')
	if cars:
		context.bot.send_message(chat_id=chat_id,
			text='<b>Редагування машин</b>', parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardMarkup([['Додати машину'], ['Повернутися в меню']], resize_keyboard=True))

		for car in cars:
			context.bot.send_message(chat_id=chat_id,
				text=car[1],
				reply_markup=InlineKeyboardMarkup([
					[InlineKeyboardButton('Видалити', callback_data='delete_car$'+str(car[0]))]
					]))
	else:
		context.bot.send_message(chat_id=chat_id,
			text='В боті ще немає машин',
			reply_markup=main_menu())


	return ConversationHandler.END


def add_driver_1(update, context):
	chat_id = update.effective_chat.id
	context.user_data['driver'] = {}

	context.bot.send_message(chat_id=chat_id,
			text='Введіть ФІО водія',
			reply_markup=back_menu())

	return states.DRIVER[0]

def add_driver_2(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END
	context.user_data['driver']['name'] = text

	context.bot.send_message(chat_id=chat_id,
			text='Введіть стаж водія',
			reply_markup=back_menu())

	return states.DRIVER[1]


def add_driver_3(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END
	try:
		int(text)
	except:
		context.bot.send_message(chat_id=chat_id,
			text='Введіть стаж водія',
			reply_markup=back_menu())

		return states.DRIVER[1] 
	else:
		context.user_data['driver']['experience'] = int(text)

		context.bot.send_message(chat_id=chat_id,
				text='Введіть номер машини',
				reply_markup=back_menu())

		return states.DRIVER[2]


def add_driver_4(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END
	context.user_data['driver']['car_number'] = text

	try:
		db.insert_driver(context.user_data['driver'])
	except:
		context.bot.send_message(chat_id=chat_id,
				text='Виникла помилка, зверніть увагу, машина повинна бути в базі та до неї ще не повинен бути прикріпленний водій',
				reply_markup=main_menu())
	else:
		context.bot.send_message(chat_id=chat_id,
				text='Дані успішно збережені',
				reply_markup=main_menu())

	
	return ConversationHandler.END



def add_car_1(update, context):
	chat_id = update.effective_chat.id
	context.user_data['car'] = {}

	context.bot.send_message(chat_id=chat_id,
			text='Введіть номер машини',
			reply_markup=back_menu())

	return states.CAR[0]



def add_car_2(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END
	context.user_data['car']['vin'] = text

	context.bot.send_message(chat_id=chat_id,
			text='Введіть назву машини',
			reply_markup=back_menu())

	return states.CAR[1]

def add_car_3(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END
	context.user_data['car']['name'] = text

	context.bot.send_message(chat_id=chat_id,
			text='Введіть тип пального',
			reply_markup=back_menu())

	return states.CAR[2]

def add_car_4(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END
	context.user_data['car']['fuel'] = text

	try:
		db.insert_car(context.user_data['car'])
	except Exception as e:
		print(e)
		context.bot.send_message(chat_id=chat_id,
				text='Виникла помилка, зверніть увагу, що номер машини повинен бути унікальним',
				reply_markup=main_menu())
	else:
		context.bot.send_message(chat_id=chat_id,
				text='Дані успішно збережені',
				reply_markup=main_menu())

	return ConversationHandler.END




def add_route_1(update, context):
	chat_id = update.effective_chat.id
	context.user_data['route'] = {}

	context.bot.send_message(chat_id=chat_id,
			text='Введіть назву маршруту',
			reply_markup=back_menu())

	return states.ROUTE[0]


def add_route_2(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END
	context.user_data['route']['name'] = text

	context.bot.send_message(chat_id=chat_id,
			text='Введіть відстань',
			reply_markup=back_menu())

	return states.ROUTE[1]

def add_route_3(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END
	
	try:
		int(text)
	except:
		context.bot.send_message(chat_id=chat_id,
			text='Введіть відстань',
			reply_markup=back_menu())

		return states.ROUTE[1]
	else:
		context.user_data['route']['distance'] = text
		context.bot.send_message(chat_id=chat_id,
				text='Введіть оплату',
				reply_markup=back_menu())

		return states.ROUTE[2]

def add_route_4(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text
	if text  == 'Повернутися в меню':
		context.bot.send_message(chat_id=chat_id,
			text='Ви повернулися в меню',
			reply_markup=main_menu())
		return ConversationHandler.END
	try:
		int(text)
	except:
		context.bot.send_message(chat_id=chat_id,
				text='Введіть оплату',
				reply_markup=back_menu())

		return states.ROUTE[2]
	else:
		context.user_data['route']['payment'] = text

		try:
			db.insert_route(context.user_data['route'])
		except Exception as e:
			print(e)
			context.bot.send_message(chat_id=chat_id,
					text='Виникла помилка',
					reply_markup=main_menu())
		else:
			context.bot.send_message(chat_id=chat_id,
					text='Дані успішно збережені',
					reply_markup=main_menu())

		return ConversationHandler.END











