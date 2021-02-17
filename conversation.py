from telegram.ext import (
	CommandHandler,
	MessageHandler,
	Filters,
	ConversationHandler,
	CallbackQueryHandler
)

import registration 
import states
import flows
import message

def cancel(update, context):
	return ConversationHandler.END

conv_handler = ConversationHandler(
		entry_points=[
			CommandHandler('start', registration.start),
			MessageHandler(Filters.text, message.handle),
			CallbackQueryHandler(message.callback),
			],
		states={
            states.REGISTRATION[0]: [
				MessageHandler(Filters.text, registration.get_password),
			],
			states.UPLOAD[0]: [
				MessageHandler(Filters.document, flows.upload_table_2),
				MessageHandler(Filters.all, flows.cancel_upload_table),
			],
			states.TRANSPORTATION[0]: [
				CallbackQueryHandler(flows.add_transportation_2)
			],
			states.TRANSPORTATION[1]: [
				CallbackQueryHandler(flows.add_transportation_3)
			],
			states.TRANSPORTATION[2]: [
				MessageHandler(Filters.text, flows.add_transportation_4),
			],
			states.TRANSPORTATION[3]: [
				MessageHandler(Filters.text, flows.add_transportation_5),
			],
			states.TRANSPORTATION[4]: [
				MessageHandler(Filters.text, flows.add_transportation_6),
			],

		},
		fallbacks=[CommandHandler('cancel', cancel)],
)
