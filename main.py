import asyncio
import logging
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import Command
from aiogram.types import FSInputFile
from datetime import datetime
import pytz

from config import BotSetings
from Handlers  import HomeWork,Schedule,register
from Handlers.States import logSates

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BotSetings.token)
dp = Dispatcher()

@dp.callback_query(F.data)
async def Choice(call: types.CallbackQuery, state: FSMContext):
    if state == logSates.Choice:
        if call.data == 'teacher':
            await call.message.answer('Enter ID')
            #await state.set_state(logSates.EnterIdT)
        if call.data == 'student':
            await call.message.answer('Enter ID')
           #await state.set_state(logSates.EnterId)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    if BotSetings.Debug:
        await start()
    dp.include_routers(register.router, HomeWork.router, Schedule.router)
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