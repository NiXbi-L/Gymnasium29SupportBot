import asyncio
import logging

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_media_photo import InputMediaType
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Handlers.States import admADDStates
from DB import DBfunc
from DB.Hashfunc import passhashing
from config import BotSetings
#from Handlers.builders import

router = Router() #Создаем объект роутер
bot = Bot(token=BotSetings.token) #Создаем объект бот

@router.message(Command('addTeach')) #Обработчик команды addTeach
async def addTeach(message: Message, state: FSMContext):
    if DBfunc.IF('adm','`FSc`',f'TelegramID = {message.from_user.id}'): #Условие наличия TelegramID в таблице администраторов
        await message.answer('Введите ФИО учителя')
        await state.set_state(admADDStates.EnterFSc) # Меняем состояние на admADDStates.EnterFSc

@router.message(admADDStates.EnterFSc) #Обработчик состояния admADDStates.EnterFSc
async def EnterFSc(message: Message,state: FSMContext):
    try:
        DBfunc.INSERT('teacher','FSc,`userkey`',f'"{message.text}","{passhashing(message.text)}"')
        await state.clear()
        await message.answer(f'Учитель создан\nkey:```{passhashing(message.text)}```',parse_mode="MarkdownV2")
    except Exception as e:
        print(e)
        await message.answer('Incorrect Value')

