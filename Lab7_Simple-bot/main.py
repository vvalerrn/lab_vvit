import telebot, psycopg2, datetime
from telebot import types

token = "5876107950:AAHDzf-7MTNgbBjpk7a4B1WLsoscaukH2Zw"
bot = telebot.TeleBot(token)

conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="kthfcfif2",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

week_num = int(datetime.datetime.utcnow().isocalendar()[1])


def even_week(week_num):
    if week_num % 2 == 0:
        return 'чётная'
    else:
        return 'нечётная'


def schedule_for_the_day(day, week):
    cursor.execute("select subject, room_numb, start_time from timetable where day=%s and week=%s order by id",
                   [str(day), str(week)])
    records = cursor.fetchall()
    string = ''

    if records:
        for i in records:
            subject, room_numb, start_time = i[0], i[1], i[2]
            cursor.execute("select full_name from teacher where subject=%s", [str(subject)])
            full_name = cursor.fetchall()
            string += str(subject) + '  Кабинет №' + str(room_numb) + '  Начало: ' + str(
                start_time) + ' Преподаватель: ' \
                      + str(full_name[0][0]) + '\n'
    else:
        string = 'Занятий нет' + '\n'

    return string


def week_schedule(week):
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    days_db = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
    string = ''
    for i in range(len(days)):
        string += str(days[i]) + " :\n" + schedule_for_the_day(str(days_db[i]), even_week(week)) + '\n'
    return string


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник")
    keyboard.row("Среда", "Четверг")
    keyboard.row("Пятница", "Суббота")
    keyboard.row("Расписание на текущую неделю")
    keyboard.row("Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Здравствуйте! Хотите узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею отображать расписание на нужный вам день или неделю. Чтобы узнать какая \
сейчас неделя, введите /week. Чтобы получить ссылку на официальный сайт МТУСИ, \
введите /mtuci')


@bot.message_handler(commands=['week'])
def week(message):
    if week_num % 2 == 0:
        bot.send_message(message.chat.id, "Чётная неделя")
    else:
        bot.send_message(message.chat.id, "Нечётная неделя")


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, "Тогда Вам сюда - https://mtuci.ru")
    elif message.text.lower() == 'понедельник':
        bot.send_message(message.chat.id, schedule_for_the_day('Пн', even_week(week_num)))
    elif message.text.lower() == 'вторник':
        bot.send_message(message.chat.id, schedule_for_the_day('Вт', even_week(week_num)))
    elif message.text.lower() == 'среда':
        bot.send_message(message.chat.id, schedule_for_the_day('Ср', even_week(week_num)))
    elif message.text.lower() == 'четверг':
        bot.send_message(message.chat.id, schedule_for_the_day('Чт', even_week(week_num)))
    elif message.text.lower() == 'пятница':
        bot.send_message(message.chat.id, schedule_for_the_day('Пт', even_week(week_num)))
    elif message.text.lower() == 'суббота':
        bot.send_message(message.chat.id, schedule_for_the_day('Сб', even_week(week_num)))
    elif message.text.lower() == 'расписание на текущую неделю':
        bot.send_message(message.chat.id, week_schedule(week_num))
    elif message.text.lower() == 'расписание на следующую неделю':
        bot.send_message(message.chat.id, week_schedule(week_num + 1))
    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.polling(none_stop=True, interval=0)
