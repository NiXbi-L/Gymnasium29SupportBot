from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, callback_query, ReplyKeyboardRemove

from DB import DBfunc
from Handlers.States import Chat
from config import BotSetings

router = Router()
bot = Bot(token=BotSetings.token)

connect1 = {}
connect2 = {}


@router.message(Command('exit'), Chat.EnterMessage)
async def exit(message: Message, state: FSMContext):
    await message.answer('Чат завершен')
    await bot.send_message(chat_id=connect1[message.from_user.id], text='Чат завершен')
    connect2.pop(connect1[message.from_user.id])
    connect1.pop(message.from_user.id)
    await state.clear()


@router.message(Command('exit'), Chat.EnterMessageUser)
async def exit(message: Message, state: FSMContext):
    await message.answer('Чат завершен')
    await bot.send_message(chat_id=connect2[message.from_user.id], text='Чат завершен')
    connect1.pop(connect2[message.from_user.id])
    connect2.pop(message.from_user.id)
    await state.clear()


@router.callback_query(lambda query: query.data.startswith('Stud_'), Chat.Choice)
async def Choice(call: callback_query, state: FSMContext):
    data = call.data.split('_')[1]
    data = await DBfunc.SELECT('TelegramID', 'student', f'FSc = "{data}"')
    data = data[0][0]
    connect1[call.from_user.id] = data
    connect2[data] = call.from_user.id
    await bot.send_message(chat_id=call.from_user.id, text='Соединение установлено.',
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=data,
                           text=f'С вами начали чат для того чтобы закрыть чат и дальше пользоваться функционалом бота введите /exit',
                           reply_markup=ReplyKeyboardRemove())
    await state.set_state(Chat.EnterMessage)


@router.message(Chat.EnterMessage)
async def EnterMessage(message: Message, state: FSMContext):
    await bot.send_message(chat_id=connect1[message.from_user.id], text=message.text)


@router.message(Chat.EnterMessageUser)
@router.message(lambda message: message.from_user.id in connect2)
async def EnterMessage(message: Message, state: FSMContext):
    FSc = await DBfunc.SELECT('FSc', 'student', f'TelegramID = {message.from_user.id}')
    FSc = FSc[0][0].split()[1]
    await bot.send_message(chat_id=connect2[message.from_user.id], text=f'{FSc}: {message.text}')
    await state.set_state(Chat.EnterMessageUser)
