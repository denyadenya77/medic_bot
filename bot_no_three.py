from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram.utils.request import Request as TelegramRequest


class ThirdMedicBot:

    (GET_USER_STATUS, GET_START_POINT, GET_FINISH_POINT, GET_DEPARTURE_DATE, GET_DEPARTURE_TIME,
     GET_RIDE_STATUS) = map(chr, range(6))
    DRIVER, DOCTOR = map(chr, range(6, 8))
    ONE_TIME, REGULAR = map(chr, range(8, 10))

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.req = TelegramRequest(
            connect_timeout=0.5,
            read_timeout=1.0,)
        self.bot = Bot(
            token=self.access_token,
            request=self.req)
        self.updater = Updater(bot=self.bot, use_context=True)

        start_handler = CommandHandler('start', self.start)

        main_conversation_handler = ConversationHandler(
            entry_points=[
                CommandHandler(command="register", callback=self.register),
                CommandHandler(command="add_one_time_ride", callback=self.add_the_ride)
            ],
            states={
                self.GET_USER_STATUS: [CallbackQueryHandler(self.get_user_status, pattern=f'^{str(self.DRIVER)}$|^{str(self.DOCTOR)}$')],
                self.GET_START_POINT: [MessageHandler(Filters.text, self.get_start_point, pass_user_data=True)],  # change to Filters.location
                self.GET_FINISH_POINT: [MessageHandler(Filters.text, self.get_finish_point, pass_user_data=True)],  # change to Filters.location
                self.GET_DEPARTURE_DATE: [MessageHandler(Filters.text, self.get_date_of_departure, pass_user_data=True)],
                self.GET_DEPARTURE_TIME: [MessageHandler(Filters.text, self.get_time_of_departure, pass_user_data=True)],
                self.GET_RIDE_STATUS: [CallbackQueryHandler(self.get_ride_status,
                                                            pattern=f'^{str(self.ONE_TIME)}$|^{str(self.REGULAR)}$',
                                                            pass_user_data=True)]
            },
            fallbacks=[[CommandHandler('cancel', self.cancel)]])

        self.updater.dispatcher.add_handler(start_handler)
        self.updater.dispatcher.add_handler(main_conversation_handler)

    def start(self, update, context):
        update.message.reply_text('Вітаємо!')

    def run_bot(self):
        self.updater.start_polling()

    def cancel(self, update, context):
        return ConversationHandler.END

    # start handler methods
    def register(self, update, context):
        text = 'Давайте знайомитися! Оберить тип користувача:'
        keyboard = [[InlineKeyboardButton("Водій", callback_data=str(self.DRIVER)),
                     InlineKeyboardButton("Лікар", callback_data=str(self.DOCTOR))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text, reply_markup=reply_markup)
        return self.GET_USER_STATUS

    def get_user_status(self, update, context):
        query = update.callback_query
        user_type = query.data
        if user_type == self.DRIVER:
            update.callback_query.answer()
            update.callback_query.edit_message_text(text=f'Вітаємо! Тепер ви наш DRIVER.')
        else:
            update.callback_query.answer()
            update.callback_query.edit_message_text(text=f'Вітаємо! Тепер ви наш DOCTOR.')
        return ConversationHandler.END

    # register_conversation_handler methods
    def add_the_ride(self, update, context):
        update.message.reply_text('Надішліть координати старту. \n51.6680, 32.6546')
        return self.GET_START_POINT

    def get_start_point(self, update, context):
        latitude, longitude = update.message.text.split(', ')
        # adding vars to user_data
        context.user_data['start_latitude'] = latitude
        context.user_data['start_longitude'] = longitude
        update.message.reply_text(f'Координати місця вашого відправлення: {latitude}, {longitude}')
        update.message.reply_text('А тепер вкажіть, куди ви прямуєте.')
        return self.GET_FINISH_POINT

    def get_finish_point(self, update, context):
        latitude, longitude = update.message.text.split(', ')
        # adding vars to user_data
        context.user_data['finish_latitude'] = latitude
        context.user_data['finish_longitude'] = longitude
        update.message.reply_text(f'Координати місця вашого призначення: {latitude}, {longitude}')
        update.message.reply_text('Будь ласка, введіть дату поїздки у форматі DD.MM.YYYY')
        return self.GET_DEPARTURE_DATE

    def get_date_of_departure(self, update, context):
        date_of_departure = update.message.text
        # adding vars to user_data
        context.user_data['date_of_departure'] = date_of_departure
        update.message.reply_text(f'Дата вашого відправлення: {date_of_departure}.'
                                  f'Залишилося визначитися з часом! Введіть час у форматі HH.MM')
        return self.GET_DEPARTURE_TIME

    def get_time_of_departure(self, update, context):
        time_of_departure = update.message.text
        # adding vars to user_data
        context.user_data['time_of_departure'] = time_of_departure

        keyboard = [[InlineKeyboardButton("Однократна поїздка", callback_data='однократна поїздка')],
                    [InlineKeyboardButton("Регулярна поїздка", callback_data='регулярна поїздка')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(f'Час вашого відправлення: {time_of_departure}.'
                                  f'Якщо ви здійснюєте цю поїздку регулярно - повідомте про це, будь ласка.',
                                  reply_markup=reply_markup)
        return self.GET_RIDE_STATUS

    def get_ride_status(self, update, context):
        update.message.reply_text('fsjlfkjsldfjlk')
        query = update.callback_query
        ride_type = query.data
        # adding vars to user_data
        if ride_type == self.ONE_TIME:
            context.user_data['ride_type'] = 'ONE_TIME'
        else:
            context.user_data['ride_type'] = 'REGULAR'
        update.callback_query.answer()
        update.callback_query.edit_message_text(f'Дякуємо! Ваша поїздка зереєстрована у системі. Ми повідомимо, коли знайдемо вам '
                                  f'попутника\n'
                                  f'Деталі:\n'
                                  f'Координати відправлення: {context.user_data["start_latitude"]}, {context.user_data["start_longitude"]}.\n'
                                  f'Координати призначення: {context.user_data["finish_latitude"]}, {context.user_data["finish_longitude"]}\n'
                                  f'Дата відправлення: {context.user_data["date_of_departure"]}.\n'
                                  f'Час выдправлення: {context.user_data["time_of_departure"]}.\n'
                                  f'Тип поїдки: {context.user_data["ride_type"]}.')
        return ConversationHandler.END


















