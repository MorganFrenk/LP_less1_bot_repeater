import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Бот который играет в города

def greet_user():
    return

def goroda_game():
    return

def main():
    # Создаю бота и передаю ему ключ
    mybot = Updater(settings.API_KEY_GORODA, use_context=True)
    
    # Добавляю диспетчера событий. (старт, сообщение с городом)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, goroda_game))

    logging.info('Бот стартовал')
    # Начинаю отправку запросов
    mybot.start_polling()
    
    # Запускаю бесконечную отправку запросов
    mybot.idle()

if __name__ == "__main__":
    main()