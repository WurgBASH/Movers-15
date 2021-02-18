from telegram import (ReplyKeyboardRemove, 
			ReplyKeyboardMarkup, 
			InlineKeyboardMarkup,
			InlineKeyboardButton,
			KeyboardButton)



def main_menu():
	return ReplyKeyboardMarkup([['Перевезення'], ['Звіти', 'Документи'], ['Налаштування']], resize_keyboard=True)

def settings_menu():
	return ReplyKeyboardMarkup([['Тарифи','Водії'], ['Маршрути','Машини'], ['Повернутися в меню']], resize_keyboard=True)

def transported_menu():
	return ReplyKeyboardMarkup([['Додати перевезення'], ['Видалити перевезення'], ['Повернутися в меню']], resize_keyboard=True)

def reports_menu():
	return ReplyKeyboardMarkup([['Відомість про ЗП водіїв'], ['Відомість про вартість перевезень'], ['Повернутися в меню']], resize_keyboard=True)

def documents_menu():
	return ReplyKeyboardMarkup([['Завантажити водіїв'], ['Завантажити маршрути'], ['Завантажити машини'], ['Повернутися в меню']], resize_keyboard=True)

def back_menu():
	return ReplyKeyboardMarkup([['Повернутися в меню']], resize_keyboard=True)





