from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from DB import DBfunc
from Handlers.States import LeaderClubStates
from Handlers.builders import mainKeyboard
from Handlers.AdminPanel.Functions import admnotification

router = Router()
@router.message(F.text == 'Подать заявку в Лидер-Клуб')
async def LeaderClubApl(message: Message, state: FSMContext):
    if await DBfunc.IF('student', '`TelegramID`', f'`TelegramID` = {message.from_user.id}'):
        userid = await DBfunc.SELECT('id', 'student', f'TelegramID = {message.from_user.id}')  # получаем userID по TelegramID
        userid = userid[0][0]
        if await DBfunc.COUNT('lcaplications', 'id', f'userid = {userid} AND `status` = "processed"') < 1:  # Если кол-во заявок меньше 1
            await message.answer('Расскажите немного о себе. (Max 300 символов)',
                                 reply_markup=ReplyKeyboardRemove())
            await state.set_state(LeaderClubStates.EnterApl)  #Переключаем состояние в LeaderClubStates.EnterApl
        else:
            await message.answer('У вас уже есть активная заявка!',
                                 reply_markup=mainKeyboard())
            await state.clear()

@router.message(LeaderClubStates.EnterApl)
async def EnterApl(message: Message, state: FSMContext):
    if len(list(message.text)) <=300: #Если длинна сообщения мееньше или ровна 300 символам и у пользователя нет открытых заявок
        userid = await DBfunc.SELECT('id', 'student', f'TelegramID = {message.from_user.id}') # получаем userID по TelegramID
        userid = userid[0][0]
        await DBfunc.INSERT('lcaplications','userid,text',f'{userid},"{message.text}"') #Создаем запись заявки в LeaderClub
        await message.answer('Ваше заявление отправлено. Как только оно будет расcмотрено вам придет уведомление!',
                                reply_markup=mainKeyboard())
        report = await admnotification(f'Поступила новая заявка на вступление!', 'LCWOffer')
        print(f'Доставлено: {report[0]}\nОшибка доставки: {report[1]}')
        await state.clear() #Отчищаем состояние
    else:
        await message.answer(f'Ваше сообщение выходит за лимит в 300 символов:\n{message.text[300::]}')