from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DB import DBfunc

router = Router()

@router.message(F.text == 'Домашнее задание')
async def HomeWork(message: Message, state: FSMContext):
    if DBfunc.IF('student', '`TelegramID`', f'`TelegramID` = {message.from_user.id}'):
        await message.answer('NetShcoolAPI Временно не доступен.')
