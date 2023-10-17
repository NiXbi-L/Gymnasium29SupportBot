from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from DB import DBfunc
from Handlers.States import AdmStates
from Handlers.builders import admSetingsKeyboard, admSetingsInline
from Handlers.AdminPanel.Functions import genButtons
from config import BotSetings

router = Router()
bot = Bot(token=BotSetings.token)


@router.message(lambda message: message.text == 'Настройки', AdmStates.Choice)
async def Setings(message: Message, state: FSMContext):
    await message.answer('Что хочешь насторить?', reply_markup=admSetingsKeyboard())


@router.message(lambda message: message.text == 'Уведомления', AdmStates.Choice)
async def notification(message: Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='Загрузка...', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)
    await message.answer('Настройки уведомлений⤵️',
                         reply_markup=admSetingsInline(await genButtons(message.from_user.id)))
    await state.set_state(AdmStates.notification)

@router.callback_query(lambda query: query.data.startswith("notification_"), AdmStates.notification)
async def notification(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')[1].split()
    buttonName = ['marcket', 'LCOffer', 'LCWOffer', 'ErrorReprort']
    for i in buttonName:
        if data[1] == i:
            if data[0] == 'Отключить':
                await DBfunc.UPDATEWHERE('adm',f'{i} = 0',f'TelegramID = {call.from_user.id}')
            else:
                await DBfunc.UPDATEWHERE('adm', f'{i} = 1', f'TelegramID = {call.from_user.id}')

    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,text='Настройки уведомлений⤵️',
                         reply_markup=admSetingsInline(await genButtons(call.from_user.id)))


