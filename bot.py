import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

# Телеграм-бот который повторяет все что ему отправили

logging.basicConfig(level=logging.INFO)

def greet_user(update, context):
    logging.info('Команда /start активирована')

    start_reply = 'Здарова!'
    update.message.reply_text(start_reply)
    logging.info('Ответ бота на /start: ' + start_reply)

def talk_to_me(update, context):
    user_text = update.message.text
    logging.info('Сообщение от пользователя: ' + user_text)
    
    standart_reply = 'Сам ты ' + user_text
    update.message.reply_text(standart_reply)
    logging.info('Ответ бота: ' + standart_reply)

def main():
    # Создаю бота и передаю ему ключ
    mybot = Updater(settings.API_KEY, use_context=True)
    
    # Добавляю диспетчера события "start" и обработчика текста
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    # Начинаю отправку запросов
    mybot.start_polling()
    
    # Запускаю бесконечную отправку запросов
    mybot.idle()

main()