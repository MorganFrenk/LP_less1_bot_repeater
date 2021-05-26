import logging
import csv
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)

# Бот который играет в города (Россия)

def greet_user(update, context):
    logging.info('Команда /start активирована')

    start_reply = 'Привет!\nЯ бот, который играет в города. \n' \
                'Правила просты: каждый участник в свою очередь' \
                'называет реально существующий город ' \
                'России, название которого начинается на ту букву, ' \
                'которой оканчивается название предыдущего. \n' \
                'Начнем? Ты первый.'

    update.message.reply_text(start_reply) 

def goroda_game(update, context):
    logging.info('Получено сообщение в goroda_game')

    user_gorod = update.message.text

    # Экспортирую список всех городов из файла в лист
    with open('goroda.csv', 'r', encoding='utf-8') as goroda_csv:
        goroda = list(csv.reader(goroda_csv))
        goroda = [i for subl in goroda for i in subl]
    
    with open(f'{settings.DATA_DEST}{settings.GORODA_BOT_DATA}', 'r+', encoding='utf-8-sig')\
        as user_data_scv:
        fields = ['User_id', 'Pass_towns']

        reader = csv.DictReader(user_data_scv)
        writer = csv.DictWriter(user_data_scv, fields)

        for row in reader:
            logging.info(row)

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