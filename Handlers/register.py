import asyncio
import logging

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_media_photo import InputMediaType
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Handlers.States import logSates
from DB import DBfunc
from config import BotSetings
from Handlers.builders import studTeachInline,regYesNoInline,regYesNoTInline

router = Router() #Создаем объект роутер
bot = Bot(token=BotSetings.token) #Создаем объект бот

@router.message(Command('start')) #Обработчик команды старт
async def start(message: Message, state: FSMContext):
    builder = studTeachInline() #Создаем объект builder
    await message.answer('dev test v0.1',reply_markup=builder.as_markup()) #Выводим сообщение с инлайн кнопками

@router.message(logSates.EnterId) #Обработчик события состояния logSates.EnterId
async def ceckid(message: Message, state: FSMContext):
    try:
        if DBfunc.IF('student','*',f'`user key` = "{message.text}" AND TelegramID != {message.from_user.id}'): #Проверяем через БД условие если key указан верно и TelegramID != UserTelegramID
            FSc = DBfunc.SELECT('`FSc`','student',f'`user key` = "{message.text}"')[0] #Получаем ФИО и id пользователя по ввведенному ключу
            await message.answer(f'Вы {FSc[1]}?',reply_markup=regYesNoInline(FSc[0]).as_markup())#Отпавляем сообщение о подтверждении
        else:
            await message.answer('Incorrect ID or User in DB.') #Выводим сообщение об ошибке о неверно введенных данных или пользователь уже в системе
    except Exception as e:
        print(e)
        await message.answer('Incorrect value. Try again') #Выводим сообщение об ошибке данных

@router.message(logSates.EnterIdT) #Обработчик события состояния logSates.EnterIdT
async def ceckid(message: Message, state: FSMContext):
    try:
        if DBfunc.IF('teacher','*',f'`userkey` = "{message.text}" AND TelegramID != {message.from_user.id}'): #Проверяем через БД условие если key указан верно и TelegramID != UserTelegramID
            FSc = DBfunc.SELECT('`id`,`FSc`','teacher',f'`userkey` = "{message.text}"')[0] # получаем ФИО и id пользователя по ключу
            await message.answer(f'Вы {FSc[1]}?',reply_markup=regYesNoTInline(FSc[0]).as_markup())
        else:
            await message.answer('Incorrect ID or User in DB.') #Выводим сообщение об ошибке о неверно введенных данных или пользователь уже в системе
    except Exception as e:
        print(e)
        await message.answer('Incorrect value. Try again') #Выводим сообщение об ошибке данных



@router.callback_query(F.data.startswith("Choice_")) #Обработчик колбеков выбора
async def Choice(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1] #Убераем тег из call.data
    if data == 'teacher':
        await state.set_state(logSates.EnterIdT) #Меняем состояние на logSates.EnterIdT
    if data == 'student':
        await state.set_state(logSates.EnterId) #Меняем состояние на logSates.EnterId
    await bot.edit_message_text(message_id=call.message.message_id,chat_id=call.from_user.id, text='Enter key') #Редактируем сообщение с кнопками и просим пользователя ввести ключь

@router.callback_query(F.data.startswith("Confirm_"))#Подтверждение Ученик
async def Confirm(call: types.callback_query, state: FSMContext):
    data = call.data.split("_")[1]  # Убераем тег из call.data
    messageText = call.data.split("_")[2]  # Достаем MessageText из data
    if data == 'yes':
        DBfunc.UPDATEWHERE('student', f'TelegramID = {call.from_user.id}',f'`id` = "{messageText}"')  # Обновляем поле TelegramID на TelegramID пользователя
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Register succesful')  # Редактируем сообщение с кнопками и просим пользователя ввести ключь
        await state.clear()
    if data == 'no':
        builder = studTeachInline() #Создем объект builder
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='dev test v0.1',reply_markup=builder.as_markup())  # Редактируем сообщение с кнопками и просим пользователя ввести ключь
        await state.set_state(logSates.Choice)

@router.callback_query(F.data.startswith("ConfirmT_"))#Подтверждение Учитель
async def Confirm(call: types.callback_query, state: FSMContext):
    data = call.data.split("_")[1]  # Убераем тег из call.data
    messageText = call.data.split("_")[2]  # Достаем MessageText из data
    if data == 'yes':
        DBfunc.UPDATEWHERE('teacher', f'TelegramID = {call.from_user.id}',f'`id` = "{messageText}"')  # Обновляем поле TelegramID на TelegramID пользователя
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Register succesful')  # Редактируем сообщение с кнопками и выводим сообщение об успешной регистрации
        await state.clear()
    if data == 'no':
        builder = studTeachInline() #Создем объект builder
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='dev test v0.1',reply_markup=builder.as_markup())  #Редактируем сообщение с кнопками и просим пользователя ввести ключь
        await state.set_state(logSates.Choice)

