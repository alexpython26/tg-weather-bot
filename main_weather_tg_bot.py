import requests
import datetime
from config import token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! напиши название города и я пришлю сводку погоды")


@dp.message_handler()
async def get_weather(message: types.Message):

    code_to_smile = {
        "Clear": 'Ясно \U00002600',
        "Clouds": 'облачно \U00002601',
        "Rain": 'дождь \U00002614',
        "Drizzle": "дождь \U00002614",

    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}"
        )
        data = r.json()

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'посмотрите сами в окно'

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestarmp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestarmp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"Погода в городе: {city}\n"
              f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Температура: {cur_weather}° {wd}\n"
              f"Влажность: {humidity}\nДавление: {pressure}\n"
              f"Воздух: {wind} {wd}\n"
              # f"Погода: {weather}\n"
              f"Восход солнца: {sunrise_timestarmp}\n"
              f"Закат солнца: {sunset_timestarmp}\n"
              f"Хорошего дня! :)")



    except Exception as ex:
        await message.reply("\U00002620  Проверьте название города")


if __name__ == '__main__':
    executor.start_polling(dp)