import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import requests
from config import TOKEN_WEATHER, TOKEN_BOT

EMOJI_CODE = {200: '⛈',
              201: '⛈',
              202: '⛈',
              210: '🌩',
              211: '🌩',
              212: '🌩',
              221: '🌩',
              230: '⛈',
              231: '⛈',
              232: '⛈',
              301: '🌧',
              302: '🌧',
              310: '🌧',
              311: '🌧',
              312: '🌧',
              313: '🌧',
              314: '🌧',
              321: '🌧',
              500: '🌧',
              501: '🌧',
              502: '🌧',
              503: '🌧',
              504: '🌧',
              511: '🌧',
              520: '🌧',
              521: '🌧',
              522: '🌧',
              531: '🌧',
              600: '🌨',
              601: '🌨',
              602: '🌨',
              611: '🌨',
              612: '🌨',
              613: '🌨',
              615: '🌨',
              616: '🌨',
              620: '🌨',
              621: '🌨',
              622: '🌨',
              701: '🌫',
              711: '🌫',
              721: '🌫',
              731: '🌫',
              741: '🌫',
              751: '🌫',
              761: '🌫',
              762: '🌫',
              771: '🌫',
              781: '🌫',
              800: '☀',
              801: '🌤',
              802: '☁',
              803: '☁',
              804: '☁'}

URL_WEATHER = 'https://api.openweathermap.org/data/2.5/weather'

bot = telebot.TeleBot(TOKEN_BOT)

keyboard = ReplyKeyboardMarkup()
keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('О проекте'))

'''Сюда добавляем клавиатуру (ReplyKeyboardMarkup, KeyboardButton)'''


@bot.message_handler(commands=['start'])
def send_about(message: Message):
    """
    На команду start отправляем сообщение
    "Отправь мне свое местоположение и я отправлю тебе погоду."
    и подключаем клавиатуру.
    """
    bot.send_message(message.chat.id, 'Отправь мне свое местоположение и я отправлю тебе погоду', reply_markup=keyboard)


@bot.message_handler(regexp='О проекте')
def send_welcome(message: Message):
    """
    При нажатии на кнопку "О проекте" отправляем сообщение
    "Бот позволяет получить погоду в текущем местоположении!
    Для получения погоды - отправь боту геопозицию.
    Погода берется с сайта https://openweathermap.org."
    и подключаем снова клавиатуру. Для обработчика сообщений
    нужно передать параметр "regexp='О проекте'". Поскольку
    нажатие на кнопку "О проекте" это сообщение, то нужно
    применять обработчик сообщений для этой функции.
    """
    bot.send_message(message.chat.id, '''
    Бот позволяет получить погоду в текущем местоположении!
    Для получения погоды - отправь боту геопозицию.
    Погода берется с сайта https://openweathermap.org
    ''', reply_markup=keyboard)


def get_weather(lat, lon):
    """
    Просто функция, которая вызывается в функции send_weather.
    Здесь надо сделать запрос погоды имея координаты(которые определяются
    в send_weather), сформировать строку как на картинке слайда
    https://disk.yandex.ru/i/J8iMnJNFzzL7SQ добавив иконки 🏙 🌡 💧 и эмодзи,
    а потом функция должна вернуть эту сформированную строку.
    """
    params = {
        'appid': TOKEN_WEATHER,
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(URL_WEATHER, params=params).json()
    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['id']
    emoji = EMOJI_CODE.get(code)
    temp = response['main']['temp']
    temp_feels = response['main']['feels_like']
    humidity = response['main']['humidity']
    text = f'''
    🏙 Погода в: {city_name}\n
    {emoji} {description}\n
    🌡 Температура {round(temp)}°C\n
    🌡 Ощущается {temp_feels}°C\n
    💧 Влажность {humidity}%. \n
'''
    return text


@bot.message_handler(content_types=['location'])
def send_weather(message: Message):
    """
    Здесь из объекта message вытаскиваем координаты местности
    и вызывая get_weather передаем вычисленные координаты. Получив от
    функции get_weather строку отправляем её пользователю и не забываем подключить клавиатуру
    при отправке сообщения.
    Самое главное, чтобы координаты добавились в объект message,
    тип контента надо указать content_types=['location'].
    И еще одно главное, возвращаемся к созданию клавиатуры.
    При добавлении клавиатуры KeyboardButton('Получить погоду', request_location=True),
    нужно включить параметр request_location, который означает,
    что при нажатии на кнопку "Получить погоду" телеграм просит
    определить текущую геолокацию. После определения геолокации
    координаты отправляются в объект message из которого вытаскиваем координаты.
    """
    lat = message.location.latitude
    lon = message.location.longitude
    text: str = get_weather(lat, lon)
    if text:
        bot.send_message(message.chat.id, text, reply_markup=keyboard)


bot.infinity_polling()
