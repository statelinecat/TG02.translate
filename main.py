import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, POGODA, URL, URL_FORECAST
import random
from datetime import datetime, timedelta


bot = Bot(token=TOKEN)

dp = Dispatcher()
API_KEY = POGODA
WEATHER_URL = URL
WEATHER_URL_FORECAST = URL_FORECAST

def get_weather(city: str, api_key: str) -> str:
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(WEATHER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Погода в Москве сейчас: {temp}°C, {description}."
    else:
        return "Не удалось получить данные о погоде."


def get_weather_tomorrow(city: str, api_key: str) -> str:
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(WEATHER_URL_FORECAST, params=params)
    if response.status_code == 200:
        data = response.json()
        tomorrow_date = (datetime.now() + timedelta(days=1)).date()
        forecast_list = data['list']

        for forecast in forecast_list:
            forecast_time = datetime.fromtimestamp(forecast['dt'])
            if forecast_time.date() == tomorrow_date and forecast_time.hour == 12:
                temp = forecast['main']['temp']
                description = forecast['weather'][0]['description']
                return f"Погода в Москве завтра: {temp}°C, {description}."

        return "Не удалось получить данные о погоде на завтра."
    else:
        return "Не удалось получить данные о погоде."

@dp.message(Command('cat'))
async def cat(message: Message):
    list = ['https://cdn.fishki.net/upload/post/2019/05/17/2980924/1-depositphotos-11856682-l-2015.jpg',
            'https://cache3.youla.io/files/images/780_780/5b/ba/5bba4723b5fc2dc012011943.jpg',
            'https://www.petalatino.com/wp-content/uploads/wash-u-victory-peta-latino.jpg']
    await message.answer_photo(photo=random.choice(list), caption="Держи котика!")
@dp.message(F.photo)
async def hiphoto(message: Message):
    list = ['Ого! Какое фото!', 'Что это?', 'Хулиганим?']
    await message.answer(random.choice(list))
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == 'Привет!')
async def hitext(message: Message):
    await message.answer("Привет! Я сообщаю информацию о погоде. Также умею выполнять команды: \n /start \n /help")

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("Я умею выполнять команды: \n /start \n /help \n /weather \n /cat")


@dp.message(Command('weather'))
async def cmd_weather(message: Message):
    weather_info = get_weather("Москва", API_KEY)
    weather_info_tom = get_weather_tomorrow("Москва", API_KEY)
    await message.answer(f'{weather_info}\n\n{weather_info_tom}')

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

@dp.message()
async def start(message: Message):
    await message.send_copy(chat_id=message.chat.id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())