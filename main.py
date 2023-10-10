import asyncio
import logging
from aiogram import Bot, Dispatcher
from datetime import datetime
import pytz

from config import BotSetings
from Handlers import register
from Handlers.HomeWork import HomeWorkHandlers
from Handlers.Schedule import ScheduleHandlers
from Handlers.Addendum import admADD,TeachADD
from Handlers.LeaderClub import LCAplications, LCWorkOffer, LCstart

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
        LCAplications.router,
        LCstart.router,
        LCWorkOffer.router
                       )
    await dp.start_polling(bot)
    if BotSetings.Debug:
        time = datetime.now(pytz.timezone('Asia/Vladivostok')).strftime('%d.%m в %H:%M')
        await bot.send_message(BotSetings.admin, f'Бот остановился {time}')

async def start():
    if BotSetings.Debug:
        time = datetime.now(pytz.timezone('Asia/Vladivostok')).strftime('%d.%m в %H:%M')
        await bot.send_message(BotSetings.admin, f'Бот запущен  {time}')


if __name__ == "__main__":
    asyncio.run(main())