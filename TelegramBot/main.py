import json
import requests
import telebot
from telebot import types

from parsing import get_teachers, get_lessons
from findpic import get_images

bot = telebot.TeleBot('7004479164:AAFnRCfKHS2_Dfkh-TqneYjAtk1SF3ytVw4')
API = '4e54eae06bc63242d9a59fa59f8f514c'
YANDEX_API_KEY = 'b1g6j0rm69v9l0g1om39'

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
item1 = types.KeyboardButton('Погода')
item2 = types.KeyboardButton('Поиск копий фотографии')
item3 = types.KeyboardButton('Расписание преподавателей')
item4 = types.KeyboardButton('Расписание групп')
item5 = types.KeyboardButton('Информация о боте')
markup.add(item1, item2, item3, item4, item5)


@bot.message_handler(commands=['start'])
def start(message):
    global markup ## глобальная переменная
    mess = 'Привет,это бот Гурс, я ваш личный помощник'

    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

teachers = {"": ""}
find_type = ""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global teachers, markup, find_type
    if message.text == 'Погода':
        bot.send_message(message.chat.id, 'Введите город:')
        bot.register_next_step_handler(message, get_weather)
    if message.text == 'Главная':

        bot.send_message(message.chat.id, 'На главную', reply_markup=markup)

    elif message.text == 'Поиск копий фотографии':
        bot.send_message(message.chat.id, 'Введите URL фотографии:')
        bot.register_next_step_handler(message, find_duplicates_and_send)


    elif message.text == 'Расписание преподавателей':
        bot.send_message(message.chat.id, 'Ожидайте, преподаватели загружаются')

        teachers = get_teachers('teach')

        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for teacher in teachers.keys():
            keyboard.add(telebot.types.KeyboardButton(teacher))

        bot.send_message(message.chat.id, 'Выберите преподавателя:', reply_markup=keyboard)

    elif message.text == 'Расписание групп':
        bot.send_message(message.chat.id, 'Ожидайте, группы загружаются')
        find_type = "stud"
        ## Получа
        teachers = get_teachers('stud')
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for teacher in teachers.keys():
            keyboard.add(telebot.types.KeyboardButton(teacher))
        keyboard.add(telebot.types.KeyboardButton("Главная"))
        bot.send_message(message.chat.id, 'Выберите группу:', reply_markup=keyboard)

    ##Если преподаватель есть в списке
    if message.text in teachers.keys():

        ## Получаем ссылку на учителя
        teacher_link = teachers[message.text]
        if find_type == 'stud':
            bot.send_message(message.chat.id, f'Вы выбрали группу {message.text}, ожидайте')
        else:
            bot.send_message(message.chat.id, f'Вы выбрали преподавателя {message.text}, ожидайте')

        ## Получаем список обьектов с расписанием
        days = get_lessons(teacher_link)

        messages = []
        msg = "Расписание:\n"
        ## Составляем рассписание в одно сообщение
        for item in days:
            if item['time']:
                msg += f"День: {item['date']} Время: {item['time']}\nЗанятие: {item['subject']}\nАудитория: {item['room']}\n\n"
                if len(msg) > 3000:  # Пример максимальной длины сообщения
                    messages.append(msg)
                    msg = "Расписание (продолжение):\n"
        # Добавить последнее сообщение, если оно не пустое
        if msg:
            messages.append(msg)
        # Отправить сообщения в телеграмм
        for msg in messages:
            bot.send_message(message.chat.id, msg, reply_markup=markup)

    elif message.text == 'Информация о боте':
        bot.send_message(message.chat.id,'Этот бот помогает с информацией о погоде, поиском копий фотографий и другими функциями.', reply_markup=markup)


def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message, f'Сейчас погода: {data["main"]["temp"]}°.\nОщущается как: {data["main"]["feels_like"]}°', reply_markup=markup)
    else:
        bot.reply_to(message, 'Город указан не верно ', reply_markup=markup)


def find_duplicates_and_send(message):
    """
    Обрабатывает сообщение с URL фотографии и ищет копии с помощью Яндекс.Картинок.
    """

    bot.send_message(message.chat.id, "Ищем фотографии, пожалуйста, подождите")

    ##Получаем спсиок ссылок
    ing_links = get_images(message.text)

    ## Выводим только 5 первых ссылок
    if ing_links:
        text = f"Найдены копии фотографии:\n"
        i=0
        for url in ing_links:
            if i<5:
                text += f"{i+1}- {url}\n"
                i+=1

        ## Отправляем сообщение пользователю
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Копии фотографии не найдены.", reply_markup=markup)


bot.polling(none_stop=True)