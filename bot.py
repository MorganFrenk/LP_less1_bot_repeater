from telegram.ext import Updater, CommandHandler
# Телеграм-бот который повторяет все что ему отправили

def greet_user():
    print("Здарова!")


def main():
    # Создаю бота и передаю ему ключ
    mybot = Updater('1838472172:AAEUSJx8Ji_jHVffAq_zV-ShR6Lcvy6NGNQ', use_context=True)
    
    # Добавляю диспетчера события "start"
    dp = mybot.dispatcher()
    dp.add_handler(CommandHandler('start', greet_user))


    # Начинаю отправку запросов
    mybot.start_polling()
    
    # Запускаю бесконечную отправку запросов
    mybot.idle()

