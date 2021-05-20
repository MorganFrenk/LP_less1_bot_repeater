import logging, datetime
import settings
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Телеграм-бот который повторяет все что ему отправили

logging.basicConfig(level=logging.INFO)


def greet_user(update, context):
    logging.info('Команда /start активирована')

    start_reply = 'Здарова!'
    update.message.reply_text(start_reply) 
    logging.info('Ответ бота на /start: ' + start_reply)


def show_star(update, context):
    logging.info('Команда /planet активирована')
    try:
        planet_name = update.message.text.split()[1].title()
    except IndexError:
        logging.error('В команду /planet не введена планета')
        update.message.reply_text('Введите название планеты') 
        return

    try:
        planet = getattr(ephem, planet_name)
    except AttributeError:
        logging.error('В команду /planet введена неверное имя планеты')
        update.message.reply_text('Введите верное имя планеты') 
        return

    star_date = str(datetime.date.today())
    star = ephem.constellation(planet(star_date))
    star_reply = 'Планета ' + planet_name + ' находится в созвездии ' + star[1]
    
    logging.info(star_reply)
    update.message.reply_text(star_reply)


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
    dp.add_handler(CommandHandler('planet', show_star))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    # Начинаю отправку запросов
    mybot.start_polling()
    
    # Запускаю бесконечную отправку запросов
    mybot.idle()

if __name__ == "__main__":
    main()