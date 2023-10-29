from datetime import datetime, date

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from Handlers.States import Planer, AdmStates
from Handlers.builders import planerYesNo, planerChange, admKeyboard
from DB import DBfunc
from config import BotSetings

router = Router()
bot = Bot(token=BotSetings.token)
newEvent = {}
daysINMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
daysINMonth4Y = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


@router.message(lambda message: message.text == 'Мероприятие', Planer.Choice)
async def Event(message: Message, state: FSMContext):
    await message.answer('Ведить дату в формате ДД ММ ГГ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Planer.EnterEvDate)


@router.message(Planer.EnterEvDate)
async def EnterEvDate(message: Message, state: FSMContext):
    try:
        data = [int(i) for i in message.text.split()]
        if data[2] % 4 == 0:
            if data[1] <= 12:
                if data[0] <= daysINMonth4Y[data[1] - 1]:
                    if data[2] >= datetime.now().year:
                        newEvent[message.from_user.id] = [date(data[2], data[1], data[0])]
                        await state.set_state(Planer.EnterEvName)
                        await message.answer('Введите название мероприятия')
                    else:
                        await message.answer('Указан прошлый год')
                else:
                    await message.answer('Неверный день')
            else:
                await message.answer('Неверный месяц')
        else:
            if data[1] <= 12:
                if data[0] <= daysINMonth[data[1] - 1]:
                    if data[2] >= datetime.now().year:
                        newEvent[message.from_user.id] = [date(data[2], data[1], data[0])]
                        await state.set_state(Planer.EnterEvName)
                        await message.answer('Введите название мероприятия')
                    else:
                        await message.answer('Указан прошлый год')
                else:
                    await message.answer('Неверный день')
            else:
                await message.answer('Неверный месяц')
    except (ValueError, TypeError):
        await message.answer('Ошибка типа данных!')


@router.message(Planer.EnterEvName)
async def EnterEvName(message: Message, state: FSMContext):
    newEvent[message.from_user.id].append(message.text)
    await message.answer('Введите описания мероприятия')
    await state.set_state(Planer.EnterNoteText)


@router.callback_query(lambda query: query.data == 'und', Planer.YesNo)
async def EnterNoteText(call: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'Дата проведения: {newEvent[call.from_user.id][0]}\n'
                                f'Название: {newEvent[call.from_user.id][1]}\n'
                                f'Описание: {newEvent[call.from_user.id][2]}',
                           reply_markup=planerYesNo())


@router.message(Planer.EnterNoteText)
async def EnterNoteText(message: Message, state: FSMContext):
    newEvent[message.from_user.id].append(message.text)
    await message.answer(
        f'Дата проведения: {newEvent[message.from_user.id][0]}\n'
        f'Название: {newEvent[message.from_user.id][1]}\n'
        f'Описание: {newEvent[message.from_user.id][2]}',
        reply_markup=planerYesNo())
    await state.set_state(Planer.YesNo)


@router.callback_query(lambda query: query.data == 'change', Planer.YesNo)
async def change(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text='Что хотите изменить?',
                                reply_markup=planerChange())


@router.callback_query(lambda query: query.data == 'Date', Planer.YesNo)
async def change(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text='Введите новую дату')
    await state.set_state(Planer.ChangeEvDate)


@router.callback_query(lambda query: query.data == 'Name', Planer.YesNo)
async def change(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text='Что хотите изменить?')
    await state.set_state(Planer.ChangeEvName)


@router.callback_query(lambda query: query.data == 'Text', Planer.YesNo)
async def change(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text='Что хотите изменить?')
    await state.set_state(Planer.ChangeNoteText)


@router.message(Planer.ChangeEvDate)
async def ChangeEvDate(message: Message, state: FSMContext):
    try:
        data = [int(i) for i in message.text.split()]
        if data[2] % 4 == 0:
            if data[1] <= 12:
                if data[0] <= daysINMonth4Y[data[1] - 1]:
                    if data[2] >= datetime.now().year:
                        newEvent[message.from_user.id][0] = date(data[2], data[1], data[0])
                        await message.answer(
                            f'Дата проведения: {newEvent[message.from_user.id][0]}\n'
                            f'Название: {newEvent[message.from_user.id][1]}\n'
                            f'Описание: {newEvent[message.from_user.id][2]}',
                            reply_markup=planerYesNo())
                        await state.set_state(Planer.YesNo)
                    else:
                        await message.answer('Указан прошлый год')
                else:
                    await message.answer('Неверный день')
            else:
                await message.answer('Неверный месяц')
        else:
            if data[1] <= 12:
                if data[0] <= daysINMonth[data[1] - 1]:
                    if data[2] >= datetime.now().year:
                        newEvent[message.from_user.id][0] = date(data[2], data[1], data[0])
                        await message.answer(
                            f'Дата проведения: {newEvent[message.from_user.id][0]}\n'
                            f'Название: {newEvent[message.from_user.id][1]}\n'
                            f'Описание: {newEvent[message.from_user.id][2]}',
                            reply_markup=planerYesNo())
                        await state.set_state(Planer.YesNo)
                    else:
                        await message.answer('Указан прошлый год')
                else:
                    await message.answer('Неверный день')
            else:
                await message.answer('Неверный месяц')
    except (ValueError, TypeError):
        await message.answer('Ошибка типа данных!')


@router.message(Planer.ChangeEvName)
async def ChangeEvName(message: Message, state: FSMContext):
    newEvent[message.from_user.id][1] = message.text
    await message.answer(
        f'Дата проведения: {newEvent[message.from_user.id][0]}\n'
        f'Название: {newEvent[message.from_user.id][1]}\n'
        f'Описание: {newEvent[message.from_user.id][2]}',
        reply_markup=planerYesNo())
    await state.set_state(Planer.YesNo)

@router.message(Planer.ChangeNoteText)
async def ChangeNoteText(message: Message, state: FSMContext):
    newEvent[message.from_user.id][2] = message.text
    await message.answer(
        f'Дата проведения: {newEvent[message.from_user.id][0]}\n'
        f'Название: {newEvent[message.from_user.id][1]}\n'
        f'Описание: {newEvent[message.from_user.id][2]}',
        reply_markup=planerYesNo())
    await state.set_state(Planer.YesNo)

@router.callback_query(lambda query: query.data == 'Schedule', Planer.YesNo)
async def Schedule(call: CallbackQuery, state: FSMContext):
    nw = newEvent[call.from_user.id]
    await DBfunc.INSERT('eventplaner','name,text,date',f'"{nw[1]}","{nw[2]}","{nw[0]}"')
    newEvent.pop(call.from_user.id)
    await bot.delete_message(chat_id=call.from_user.id,
                                message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id,
                            text='Мероприятие запланировано.',
                            reply_markup=admKeyboard())
    await state.set_state(AdmStates.Choice)


