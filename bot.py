import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Телеграм-бот который повторяет все что ему отправили

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print("Запущен /start")
    update.message.reply_text('Здарова!')


def main():
    # Создаю бота и передаю ему ключ
    mybot = Updater('1838472172:AAEUSJx8Ji_jHVffAq_zV-ShR6Lcvy6NGNQ', use_context=True)
    
    # Добавляю диспетчера события "start"
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))

    logging.info('Бот стартовал')
    # Начинаю отправку запросов
    mybot.start_polling()
    
    # Запускаю бесконечную отправку запросов
    mybot.idle()

main()