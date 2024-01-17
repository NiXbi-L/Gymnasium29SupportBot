from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from DB import DBfunc
from Handlers.States import LeaderClubStates
from Handlers.builders import mainKeyboard
from Handlers.ERROR_Report.Fuctions import Hours
from config import KDA

from datetime import datetime

router = Router()

@router.message(lambda message: message.text == 'Предложить идею', LeaderClubStates.Choice)
async def idea(message: Message, state: FSMContext):
    if await DBfunc.IF('student', '`TelegramID`', f'`TelegramID` = {message.from_user.id}'):
        userid = await DBfunc.SELECT('id', 'student', f'TelegramID = {message.from_user.id}')
        userid = userid[0][0]
        if await DBfunc.COUNT('lcidea', 'id', f'userid = {userid} AND status = "processed"') < 1:
            if not (await DBfunc.IF('lcidea', '*',
                                    f'userid = {userid} AND date >= DATE_SUB(NOW(), INTERVAL {KDA.LC} HOUR) AND (status = "approved" OR status = "rejected")')):
                await state.set_state(LeaderClubStates.EnterIdea)
                await message.answer('Напиши что ты хочешь предложить. (Max 300 символов)',
                                     reply_markup=ReplyKeyboardRemove())
            else:
                date = await DBfunc.SELECT('date', 'lcidea',
                                           f'userid = {userid} AND date >= DATE_SUB(NOW(), INTERVAL {KDA.LC} HOUR) AND (status = "approved" OR status = "rejected")')
                date = date[0][-1]
                await message.answer(
                    f'Вы не можете предлогать идеи еще {await Hours((KDA.LC * 3600 - (datetime.now() - date).total_seconds()))}')

        else:
            await message.answer('У вас уже есть активная заявка',
                                 reply_markup=mainKeyboard())
            await state.clear()

@router.message(LeaderClubStates.EnterIdea)
async def EnterIdea(message: Message, state: FSMContext):
    if len(list(message.text)) <= 300:
        userid = await DBfunc.SELECT('id', 'student', f'TelegramID = {message.from_user.id}')
        userid = userid[0][0]
        await DBfunc.INSERT('lcidea','userid,text',f'{userid},"{message.text}"') #Создаем запись о заявке пользователя
        await message.answer('Ваша заявка отправлена!',
                                 reply_markup=mainKeyboard())
        await state.clear()


    else:
        await message.answer(f'Ваше сообщение выходит за лимит в 300 символов:\n```{message.text[300::]}```\nПопробуйте еще раз',parse_mode="MarkdownV2")