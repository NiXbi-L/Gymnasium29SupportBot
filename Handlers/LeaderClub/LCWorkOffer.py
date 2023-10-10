from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,ReplyKeyboardRemove

from Handlers.States import LeaderClubStates
from Handlers.builders import mainKeyboard
from DB import DBfunc

router = Router()
@router.message(F.text == 'Подать заявку в Лидер-Клуб')
async def LeaderClubApl(messge: Message, state: FSMContext):
    await messge.answer('Расскажите немного о себе. (Max 300 символов)',
                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(LeaderClubStates.EnterApl) #Переключаем состояние в LeaderClubStates.EnterApl

@router.message(LeaderClubStates.EnterApl)
async def EnterApl(message: Message, state: FSMContext):
    if len(list(message.text)) <=300: #Если длинна сообщения мееньше или ровна 300 символам и у пользователя нет открытых заявок
        userid = DBfunc.SELECT('id', 'student', f'TelegramID = {message.from_user.id}')[0][0]  # получаем userID по TelegramID
        if DBfunc.COUNT('lcaplications', 'id', f'userid = {userid} AND `status` = ') < 1: #Если кол-во заявок меньше 1
            DBfunc.INSERT('lcaplications','userid,text',f'{userid},"{message.text}"') #Создаем запись заявки в LeaderClub
            await message.answer('Ваше заявление отправлено. Как только оно будет расcмотрено вам придет уведомление!',
                                reply_markup=mainKeyboard())
            await state.clear() #Отчищаем состояние
        else:
            await message.answer('У вас уже есть активная заявка!',
                                 reply_markup=mainKeyboard())
            await state.clear()
    else:
        await message.answer(f'Ваше сообщение выходит за лимит в 300 символов:\n{message.text[300::]}')