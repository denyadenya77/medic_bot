from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
import os
from dotenv import load_dotenv
load_dotenv()


GET_REGISTER_DATA, GET_START_POINT, GET_RIDE_TYPE = map(chr, range(3))
DRIVER, DOCTOR = map(chr, range(3, 5))
ONE_TIME, REGULAR = map(chr, range(5, 7))


def cancel(update, context):
    return ConversationHandler.END


def register(update, context):
    text = 'Enter user type:'
    buttons = [[
        InlineKeyboardButton(text='DRIVER', callback_data=str(DRIVER)),
        InlineKeyboardButton(text='DOCTOR', callback_data=str(DOCTOR))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=keyboard)
    return GET_REGISTER_DATA


def get_user_status(update, context):
    user_type = update.callback_query.data

    if user_type == DRIVER:
        text = 'Now you are a DRIVER'
        update.callback_query.answer()
        update.callback_query.edit_message_text(text)
    elif user_type == DOCTOR:
        text = 'Now you are a DOCTOR'
        update.callback_query.answer()
        update.callback_query.edit_message_text(text)
    return ConversationHandler.END


def add_one_time_ride(update, context):
    update.message.reply_text('Enter start point:')
    return GET_START_POINT


def get_start_point(update, context):
    text = 'Enter ride type:'
    buttons = [[
        InlineKeyboardButton(text='ONE_TIME', callback_data=str(ONE_TIME)),
        InlineKeyboardButton(text='REGULAR', callback_data=str(REGULAR))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=keyboard)
    return GET_RIDE_TYPE


def get_ride_status(update, context):
    user_type = update.callback_query.data

    if user_type == ONE_TIME:
        text = 'You add a ONE_TIME ride.'
        update.callback_query.answer()
        update.callback_query.edit_message_text(text)
    elif user_type == REGULAR:
        text = 'You add a REGULAR ride.'
        update.callback_query.answer()
        update.callback_query.edit_message_text(text)
    return ConversationHandler.END


def main():

    updater = Updater(os.getenv("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register),
                      CommandHandler('add_one_time_ride', add_one_time_ride)],
        states={
            GET_REGISTER_DATA: [CallbackQueryHandler(get_user_status, pattern=f'^{str(DRIVER)}$|^{str(DOCTOR)}$')],
            GET_START_POINT: [MessageHandler(Filters.text, get_start_point)],
            GET_RIDE_TYPE: [CallbackQueryHandler(get_ride_status, pattern=f'^{str(ONE_TIME)}$|^{str(REGULAR)}$')]
        },

        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
