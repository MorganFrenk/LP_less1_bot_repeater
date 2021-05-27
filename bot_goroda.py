import logging
import csv
import pickle
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
                'Начнем? Ты первый. Просто напиши название города'

    update.message.reply_text(start_reply) 

def goroda_game(update, context):
    logging.info('Получено сообщение в goroda_game')

    user_gorod_input = update.message.text
    user_chat_id = update.message.chat_id
    pass_goroda_dict = {} # Словарь для хранение выбывших городов юзера

    # Экспортирую список всех городов из csv в лист
    with open('goroda.csv', 'r', encoding='utf-8') as goroda_csv:
        goroda = list(csv.reader(goroda_csv))
        goroda = [gor for gorsublist in goroda for gor in gorsublist]
    
    try:
        with open('users_pass_goroda.pickle', 'rb') as pickle_goroda:
            pass_goroda_dict = pickle.load(pickle_goroda)

            if user_chat_id not in pass_goroda_dict:
                pass_goroda_dict[user_chat_id] = [] # Добавляю нового юзера и пустой список городов
                
            logging.info(f'Выгрузка выбывших городов из pickle успешна: {pass_goroda_dict}')

    except FileNotFoundError:
        with open('users_pass_goroda.pickle', 'wb') as pickle_goroda:
            logging.info('Нет pickle с выбывшими городами. Создается')
            pass_goroda_dict[user_chat_id] = []
            pickle.dump(pass_goroda_dict, pickle_goroda)
            logging.info(f'Новый pickle записан: {pass_goroda_dict}')

    if user_gorod_input not in goroda:
        logging.info(f'Город некорректный: {user_gorod_input}')
        update.message.reply_text('Нет такого города!') 
        return

    if user_gorod_input in pass_goroda_dict[user_chat_id]:
        logging.info('Введенный город юзера выбыл из игры')
        update.message.reply_text('Этот город уже был!') 
        return

    logging.info(f'Корректный город юзера: {user_gorod_input}')
    pass_goroda_dict[user_chat_id].append(user_gorod_input) # Добавляю корректный город юзера в выбывшие

    for gorod in goroda:
        if gorod[0].lower() == user_gorod_input[-1] and gorod not in pass_goroda_dict[user_chat_id]:
            reply_gorod = gorod
            update.message.reply_text(reply_gorod) 
            logging.info(f'Ответ бота: {reply_gorod}')
            pass_goroda_dict[user_chat_id].append(reply_gorod) # Добавляю город бота в выбывшие
            break


    

    with open('users_pass_goroda.pickle', 'wb') as pickle_goroda:
        pickle.dump(pass_goroda_dict, pickle_goroda)
        logging.info(f'Pickle записан: {pass_goroda_dict}')

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