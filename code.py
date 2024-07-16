# Пишем с помощью библиотеки telegram.ext

import logging
from telegram import Update,  ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from random import choice

# Создание клавиатуры с выбором цвета карты
custom_keyboard_question = [['🟥'], ['⬛']]

# Создание клавиатуры с выбором новой игры
custom_keyboard_start = [['Играть снова!'], ['Спасибо за игру!']]

# Настроить ведение журнала
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Определить функции для обработки команды «/start» (запускаем бота)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 1 - Приветствие.
    reply_markup = ReplyKeyboardRemove()
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Добро пожаловать в игру!', reply_markup=reply_markup)

    # 2 - Правила игры.
    await context.bot.send_message(chat_id=update.effective_chat.id, text='В этой игре тебе нужно отгадать цвет масти выбранной мною карты.')

    # 3 - Создаем переменные и задаем им значения.
    context.user_data['CARD_NUMBER'] = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т')
    context.user_data['CARD_SUIT'] = ('Буби', 'Черви', 'Пики', 'Трефы')
    context.user_data['random_card_number'] = choice(context.user_data['CARD_NUMBER'])
    context.user_data['random_card_suit'] = choice(context.user_data['CARD_SUIT'])

    # 4 -> 5 - Вопрос игроку.
    reply_markup = ReplyKeyboardMarkup(custom_keyboard_question, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Введите или выберите цвет масти карты (Красный или Черный).', reply_markup=reply_markup)

# Определить функции для обработки команд «/message_handler» (принимаем сообщения пользователя)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 3 (Дублируем).
    context.user_data['CARD_NUMBER'] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'В', 'Д', 'К', 'Т']
    context.user_data['CARD_SUIT'] = ['Буби', 'Черви', 'Пики', 'Трефы']
    context.user_data['random_card_number'] = choice(context.user_data['CARD_NUMBER'])
    context.user_data['random_card_suit'] = choice(context.user_data['CARD_SUIT'])

    # 6 - Обработка ответа игрока.
    # Если правильный цвет красный
    if update.message.text == '🟥' and context.user_data['random_card_suit'] in ['Буби', 'Черви'] or update.message.text.upper() == 'КРАСНЫЙ' and context.user_data['random_card_suit'] in ['Буби', 'Черви']:
        reply_markup = ReplyKeyboardRemove()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Правильно! Загаданная карта была: {context.user_data['random_card_number']} {context.user_data['random_card_suit']}.', reply_markup=reply_markup)
        reply_markup = ReplyKeyboardMarkup(custom_keyboard_start, resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Хотите сыграть снова?', reply_markup=reply_markup)
    # Если правильный цвет черный
    elif update.message.text == '⬛' and context.user_data['random_card_suit'] in ['Пики', 'Трефы'] or update.message.text.upper() == 'ЧЕРНЫЙ' and context.user_data['random_card_suit'] in ['Пики', 'Трефы']:
        reply_markup = ReplyKeyboardRemove()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Правильно! Загаданная карта была: {context.user_data['random_card_number']} {context.user_data['random_card_suit']}.', reply_markup=reply_markup)
        reply_markup = ReplyKeyboardMarkup(custom_keyboard_start, resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Хотите сыграть снова?', reply_markup=reply_markup)
    # Если игрок захочет сыграть снова
    elif update.message.text == 'Играть снова!':
        reply_markup = ReplyKeyboardMarkup(custom_keyboard_question, resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Введите или выберите цвет масти карты (Красный или Черный).', reply_markup=reply_markup)
    # Если игрок наигрался
    elif update.message.text == 'Спасибо за игру!':
        reply_markup = ReplyKeyboardRemove()
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Если захотите сыграть еще раз, нажмите /start', reply_markup=reply_markup)
    # Если игрок не угадал цвет
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Неправильно! Загаданная карта была: {context.user_data['random_card_number']} {context.user_data['random_card_suit']}.')
    
# Определить функции для обработки неизвестных команд
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Извините, я не знаю такую команду.')

if __name__ == '__main__':

    # Настроить Telegram-бот (Вставьте ваш токен вместо YOURTOKEN)
    application = ApplicationBuilder().token('YOURTOKEN').build()

    # Добавить обработчик команды «/start»
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Добавить обработчик текстовых сообщений «/message_handler»
    application.add_handler(MessageHandler(filters.TEXT, message_handler))

    # Добавить неизвестный обработчик команд
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    # Запустить робота и ждать прихода сообщения
    application.run_polling()
 # type: ignore
