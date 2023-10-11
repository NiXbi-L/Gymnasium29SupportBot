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
from Handlers.builders import undoInline

router = Router() #Создаем объект роутер
bot = Bot(token=BotSetings.token) #Создаем объект бот

@router.message(Command('addTeach')) #Обработчик команды addTeach
async def addTeach(message: Message, state: FSMContext):
    if DBfunc.IF('adm','`FSc`',f'TelegramID = {message.from_user.id}'): #Условие наличия TelegramID в таблице администраторов
        await message.answer('Введите ФИО учителя',reply_markup=undoInline().as_markup())
        await state.set_state(admADDStates.EnterFSc) # Меняем состояние на admADDStates.EnterFSc

@router.message(admADDStates.EnterFSc) #Обработчик состояния admADDStates.EnterFSc
async def EnterFSc(message: Message,state: FSMContext):
    try:
        DBfunc.INSERT('teacher','FSc,`userkey`',f'"{message.text}","{passhashing(message.text)}"') #Добавляем пользователя в БД
        await state.clear() #отчищаем сосотяние
        await message.answer(f'Учитель создан\nkey:```{passhashing(message.text)}```', parse_mode="MarkdownV2")
    except Exception as e:
        print(e)
        await message.answer('Incorrect Value') #Выводим сообшение об ощибке

@router.message(Command('addStud'))
async def addStud(message: Message, state: FSMContext):
    if DBfunc.IF('adm', '`FSc`',f'TelegramID = {message.from_user.id}'):  # Условие наличия TelegramID в таблице администраторов
        await message.answer('Введите данные в следующем формате:\n'
                             'ФИО_Класс',reply_markup=undoInline().as_markup())
        await state.set_state(admADDStates.EnterData) #Устанавливаем состояние EnterData

@router.message(admADDStates.EnterData) # Обработчик состояния EnterData
async def EnterData(message: Message, state: FSMContext):
    data = message.text.split('_') #Парсим введенные данные
    if DBfunc.IF('class', '`id`', f'`ClassName` = "{data[1]}"'): #Если имя класса существует
        classID = DBfunc.SELECT('`id`','class',f'`ClassName` = "{data[1]}"')[0][0] #Получаем ClassID
        DBfunc.INSERT('student','`ClassID`,`FSc`,`user key`',f'"{classID}","{data[0]}","{passhashing(data[0])}"') #Добавляем пользователя в БД
        await message.answer(f'Ученик создан\nkey: ```{passhashing(data[0])}```',parse_mode="MarkdownV2")
        await state.clear() #Отчищаем состояние
    else:
        await message.answer('Такого класса не существует',reply_markup=undoInline().as_markup())

@router.callback_query(admADDStates.EnterData)
async def EnterData(message: Message,call: types.CallbackQuery,state: FSMContext):
    if call.data == 'undo':
        await state.clear()
        await call.answer('Действие отменено')

