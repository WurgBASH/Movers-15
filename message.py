from buttons import main_menu, settings_menu, transported_menu, reports_menu, documents_menu
from telegram.ext import ConversationHandler
import flows
from db import *

def handle(update, context):
	chat_id = update.effective_chat.id
	text = update.message.text

	#Меню
	if text == 'Перевезення':
		context.bot.send_message(chat_id=chat_id,
			text='Оберіть пункт меню',
			reply_markup=transported_menu())
	elif text == 'Звіти':
		context.bot.send_message(chat_id=chat_id,
			text='Оберіть звіт для завантаження',
			reply_markup=reports_menu())
	elif text == 'Документи':
		context.bot.send_message(chat_id=chat_id,
			text='Оберіть документ для завантаження',
			reply_markup=documents_menu())
	elif text == 'Налаштування':
		context.bot.send_message(chat_id=chat_id,
			text='Оберіть сутність для редагування',
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

	elif text == 'Відомість про ЗП водіїв':
		return flows.griver_payments(update, context)
	elif text == 'Відомість про вартість перевезень':
		return flows.transportation_payments(update, context)

	elif text == 'Тарифи':
		return flows.change_tarif(update, context)
	elif text == 'Водії':
		return flows.get_all_drivers(update, context)
	elif text == 'Маршрути':
		return flows.get_all_routes(update, context)
	elif text == 'Машини':
		return flows.get_all_cars(update, context)

	elif text == 'Додати водія':
		return flows.add_driver_1(update, context)
	elif text == 'Додати машину':
		return flows.add_car_1(update, context)
	elif text == 'Додати маршрут':
		return flows.add_route_1(update, context)

	
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
	elif wm_command[0] == 'delete_route':
		obj_id = int(wm_command[1])
		try:
			test = db.execute('DELETE FROM routes WHERE route_id = %d;'%obj_id)
		except:
			update.callback_query.message.edit_text('Виникла помилка')
		else:
			update.callback_query.message.edit_text('Успішно видален')
	elif wm_command[0] == 'delete_driver':
		obj_id = int(wm_command[1])
		try:
			test = db.execute('DELETE FROM drivers WHERE driver_id = %d;'%obj_id)
		except:
			update.callback_query.message.edit_text('Виникла помилка')
		else:
			update.callback_query.message.edit_text('Успішно видален')
	elif wm_command[0] == 'delete_car':
		obj_id = wm_command[1]
		try:
			test = db.execute('DELETE FROM cars WHERE car_number = \'%s\';'%obj_id)
		except:
			update.callback_query.message.edit_text('Виникла помилка')
		else:
			update.callback_query.message.edit_text('Успішно видален')


	return ConversationHandler.END







