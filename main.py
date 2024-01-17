import asyncio
import logging
from datetime import datetime

import pytz
from aiogram import Bot, Dispatcher

from Handlers import register
from Handlers.Addendum import admADD
from Handlers.HomeWork import HomeWorkHandlers
from Handlers.LeaderClub import LCstart
from Handlers.Schedule import ScheduleHandlers
from Handlers.ERROR_Report import ERROR_Handlers
from Handlers.AdminPanel import AdmPanelCall
from Handlers.Chat import messager
from Handlers.Planer import StartPlaner
from config import BotSetings

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BotSetings.token)
dp = Dispatcher()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    if BotSetings.Debug:
        await start()
    dp.include_routers(
        register.router,
        HomeWorkHandlers.router,
        ScheduleHandlers.router,
        admADD.router,
        LCstart.router,
        ERROR_Handlers.router,
        messager.router,
        AdmPanelCall.router,
        StartPlaner.router
                       )
    # Запускаем Clocker() в асинхронном режиме
    asyncio.create_task(Clocker())
    await dp.start_polling(bot)
    if BotSetings.Debug:
        time = datetime.now(pytz.timezone('Asia/Vladivostok')).strftime('%d.%m в %H:%M')
        await bot.send_message(BotSetings.admin, f'Бот остановился {time}')

async def start():
    if BotSetings.Debug:
        time = datetime.now(pytz.timezone('Asia/Vladivostok')).strftime('%d.%m в %H:%M')
        await bot.send_message(BotSetings.admin, f'Бот запущен  {time}')

async def Clocker():
    while True:

        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())