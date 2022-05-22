import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)



@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!")



@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь, зонтик - ваш главный помощник\U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]

        cur_weather = data["main"]["temp"]
        cur_weather1 = int(cur_weather)
        if cur_weather1 > 30:
            feedback = "На улице жарищее! Эрлан кричит: ""Далой одежду!!"""
        elif cur_weather1 < 30 and cur_weather1 > 15:
            feedback = "На улице тепло! Одевайтесь как хотите!"
        elif cur_weather1 < 15 and cur_weather1 > 0:
            feedback = "На улице прохладно! Нурислам советует одеться потеплее!!"
        elif cur_weather1 < 0 and cur_weather1 > -15:
            feedback = "На улице холодно! Нурсултан напоминает надеть шапку!!"
        elif cur_weather1 < -15 and cur_weather1 > -30:
            feedback = "На улице холодрыга! Тынчтык советует одеться максимально тепло, будто едешь на Северный полюс!!"


        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"



        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather1}°C {wd}\n Совет: {feedback}\n"

              f"Хорошего дня!"
              )


    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)
