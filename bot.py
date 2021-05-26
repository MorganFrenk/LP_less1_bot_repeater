import datetime
import logging
import settings
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Телеграм-бот который повторяет все что ему отправили

logging.basicConfig(level=logging.INFO)


def greet_user(update, context):
    logging.info('Команда /start активирована')

    start_reply = 'Здарова!'
    update.message.reply_text(start_reply) 
    logging.info(f'Ответ бота на /start: {start_reply}')


def show_star(update, context):
    logging.info('Команда /star активирована')
    try:
        body_name = update.message.text.split()[1].title()
    except IndexError:
        logging.error('В команду /star не введено небесное тело')
        update.message.reply_text('Введите название небесного тела (/star "имя небесного тела")') 
        return

    try:
        body = getattr(ephem, body_name)
    except AttributeError:
        logging.error('В команду /star введено неверное имя небесного тела')
        update.message.reply_text('Введите правильное имя небесного тела (/star "имя небесного тела")') 
        return

    star_date = str(datetime.date.today())
    star = ephem.constellation(body(star_date))
    star_reply = f'Небесное тело {body_name} находится в созвездии {star[1]}'
    
    logging.info(f'Ответ бота: {star_reply}')
    update.message.reply_text(star_reply)

def next_full_moon(update, context):
    logging.info('Команда /next_full_moon активирована')

    try:
        date_str = update.message.text.split()[1]
    except IndexError:
        logging.error('В команду /next_full_moon не введена дата')
        update.message.reply_text('Введите дату (/next_full_moon "дата: 2000/01/01")') 
        return

    try:
        date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
    except ValueError:
        logging.error('В команду /next_full_moon введена дата неверного формата')
        update.message.reply_text('Введите дату формата "2000/01/01"') 
        return

    next_moon_date = ephem.next_full_moon(date)
    logging.info(f'Ответ бота: {next_moon_date}')
    update.message.reply_text(f'Дата и время следующего полнолуния: {next_moon_date}')

def talk_to_me(update, context):
    user_text = update.message.text
    logging.info(f'Сообщение от пользователя: {user_text}')
    
    standart_reply = f'Сам ты {user_text}' 
    update.message.reply_text(standart_reply)
    logging.info(f'Ответ бота: {standart_reply}')


def main():
    # Создаю бота и передаю ему ключ
    mybot = Updater(settings.API_KEY_REPEATER, use_context=True)
    
    # Добавляю диспетчера событий. (start, star, next_full_moon, сообщение)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('star', show_star))
    dp.add_handler(CommandHandler('next_full_moon', next_full_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    # Начинаю отправку запросов
    mybot.start_polling()
    
    # Запускаю бесконечную отправку запросов
    mybot.idle()

if __name__ == "__main__":
    main()