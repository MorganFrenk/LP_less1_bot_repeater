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
                'Начнем? Ты первый. Просто напиши название города.'

    update.message.reply_text(start_reply) 

    # Очищаю юзер дата юзера для новой игры
    user_chat_id = update.message.chat_id
    try:
        with open('users_pass_goroda.pickle', 'rb') as pickle_goroda:
                user_data_dict = pickle.load(pickle_goroda)
        with open('users_pass_goroda.pickle', 'wb') as pickle_goroda:
                user_data_dict[user_chat_id] = {}
                pickle.dump(user_data_dict, pickle_goroda)
        
        logging.info('Pickle очищен')

    except FileNotFoundError:
        return

def goroda_game(update, context):
    logging.info('Получено сообщение в goroda_game')

    user_gorod_input = update.message.text
    user_chat_id = update.message.chat_id

    # Пустой словарь с юзер дата и вложения
    user_data_dict = {} 
    pass_goroda = []
    bot_prev_gorod = ''
    
    wrong_letters = ['ь','ъ']

    # Экспортирую список всех городов из csv в лист
    with open('goroda.csv', 'r', encoding='utf-8') as goroda_csv:
        goroda = list(csv.reader(goroda_csv))
        goroda = [gor for gorsublist in goroda for gor in gorsublist]
    
    # Загружаю pickle с юзер датой и выгружаю ее
    try:
        with open('users_pass_goroda.pickle', 'rb') as pickle_goroda:
            user_data_dict = pickle.load(pickle_goroda)

            try:
                if user_chat_id not in user_data_dict:
                    user_data_dict[user_chat_id] = {} 

                else:
                    bot_prev_gorod = user_data_dict[user_chat_id]['prev_bot_gorod']
                    pass_goroda = user_data_dict[user_chat_id]['pass_goroda']
                    logging.info(f'Выгрузка выбывших городов из pickle успешна: {user_data_dict}')
            except KeyError:
                    pass
            
    except FileNotFoundError:
        logging.info('Нет pickle с юзер дата')
        user_data_dict[user_chat_id] = {} 
        pass

    if user_gorod_input not in goroda:
        logging.info(f'Город юзера некорректный: {user_gorod_input}')
        update.message.reply_text('Нет такого города!') 
        return

    if user_gorod_input in pass_goroda:
        logging.info('Введенный город юзера выбыл из игры')
        update.message.reply_text('Этот город уже был!') 
        return

    if user_data_dict[user_chat_id]:
        if user_gorod_input[0].lower() != bot_prev_gorod[-1]:
            logging.info('Введенный город юзера противоречит правилам')
            update.message.reply_text('Этот город не подходит!') 
            return

    logging.info(f'Корректный город юзера: {user_gorod_input}')
    pass_goroda.append(user_gorod_input)

    user_gorod_input_l_let = user_gorod_input[-1]

    # Если город юзера оканчивается на букву ь или ъ, выбираем предпоследнюю букву для игры
    if user_gorod_input[-1] in wrong_letters:
        user_gorod_input_l_let = user_gorod_input[-2]
        logging.info(f'Последняя буква города юзера {user_gorod_input} некорректная')

    logging.info(f'Последняя буква города юзера {user_gorod_input_l_let}')

    for gorod in goroda:
        if gorod[0].lower() == user_gorod_input_l_let and gorod not in pass_goroda:
            bot_gorod = gorod

            update.message.reply_text(bot_gorod) 
            logging.info(f'Ответ бота: {bot_gorod}')

            pass_goroda.append(bot_gorod)
            
            # Если город бота заканчивается на некорректную для игры букву, то обрезаю ее
            if bot_gorod[-1] in wrong_letters:
                logging.info(f'Последняя буква города бота {bot_gorod} некорректа. Принимается как {bot_gorod[-2]}')
                bot_gorod = bot_gorod.rstrip(bot_gorod[-1])
            break

    # Сохраняю юзер дату в pickle
    with open('users_pass_goroda.pickle', 'wb') as pickle_goroda:
        user_data_dict[user_chat_id]['pass_goroda'] = pass_goroda
        user_data_dict[user_chat_id]['prev_bot_gorod'] = bot_gorod

        pickle.dump(user_data_dict, pickle_goroda)
        logging.info(f'Pickle записан: {user_data_dict}')

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