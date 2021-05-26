import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)

# Бот который играет в города (Россия)

def greet_user(update, context):
    logging.info('Команда /start активирована')

    start_reply = 'Привет!\nЯ бот, который играет в города. \n' \
                'Правила просты: каждый участник в свою очередь называет реально существующий город ' \
                'России, название которого начинается на ту букву, ' \
                'которой оканчивается название предыдущего. \n' \
                'Начнем? Ты первый.'

    update.message.reply_text(start_reply) 
    return

def goroda_game(update, context):
    logging.info('Получено сообщение в goroda_game')
    return

def main():
    # Создаю бота и передаю ему ключ
    mybot = Updater(settings.API_KEY_GORODA, use_context=True)
    
    # Добавляю диспетчера событий. (старт, сообщение)
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