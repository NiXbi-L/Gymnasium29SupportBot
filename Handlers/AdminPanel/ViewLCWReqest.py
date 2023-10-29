from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery


from DB import DBfunc
from Handlers.States import AdmStates, ViewLCWRequest
from Handlers.builders import mainKeyboard, admKeyboard, ViewOutputInline, ViewOutputOfferInline
from config import BotSetings
from Handlers.AdminPanel.Functions import SearchUserDataAtApl, sendNewApl

router = Router()
bot = Bot(token=BotSetings.token)

rjApl = {}

@router.message(lambda message: message.text == 'Заявки в ЛК', AdmStates.Choice)
async def Choice(message: Message, state: FSMContext):
    apll = await DBfunc.SELECT('*', 'lcaplications', f'status = "processed"')  # Запрашиваем все заявки по статусу
    if len(apll) != 0:
        apl = apll[0]
        await message.answer('Загрузка...', reply_markup=ReplyKeyboardRemove())  # Отправляем сообщение для удаления клавиатуры

        funcReturn = await SearchUserDataAtApl(apl)
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=message.message_id+1) #Удаляем сообщение
        await message.answer(f'AplicationID: {apl[0]}\n'
                             f'ФИО: {funcReturn[0][2]}\n'
                             f'Класс: {funcReturn[1]}\n'
                             f'О себе:\n{apl[2]}',
                             reply_markup=ViewOutputOfferInline(message.from_user.id))
        await state.set_state(ViewLCWRequest.View)
    else:
        await message.answer('По вашему запросу ничего не найдено',
                             reply_markup=admKeyboard())
        await state.set_state(AdmStates.Choice)

@router.callback_query(lambda query: query.data.startswith('Aprove_'), ViewLCWRequest.View) #Если заявку одобрили
async def Aprove(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1::]
    apll = await DBfunc.SELECT('*', 'lcaplications', f'status = "processed"') #Запрашиваем все заявки по статусу
    apl = apll[0]
    await DBfunc.UPDATEWHERE('lcaplications', 'status = "aproved"', f'id = {apl[0]}') #Обновляем данные в БД
    UserData = await DBfunc.SELECT('*', 'student', f'id = {apl[1]}') # Запрашиваем данные пользователя
    UserData = UserData[0]
    try:
        await bot.send_message(chat_id=UserData[3], text=f'Здравствуйте {UserData[2]}. Ваше заявление №{apl[0]} одобрено!\n'
                                                            f'Cсылка: https://t.me/+_2swjbbvnE1lOGQy\n'
                                                            f'Вступайте в группу и ждите дальнейший указаний.') #Отправляем ему уведомление
    except:
        await bot.send_message(chat_id=call.from_user.id, text='Бот заблокирован пользователем!') #Если боту не удалось отправить сообщение

    await sendNewApl(apll, data, call)

@router.callback_query(lambda query: query.data.startswith('Reject_'), ViewLCWRequest.View) #Если заявку одобрили
async def Reject(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1::]
    rjApl[call.from_user.id] = await DBfunc.SELECT('*', 'lcaplications', f'status = "processed"')  # Запрашиваем все заявки по статусу

    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text='Введите комментарий')
    await state.set_state(AdmStates.EnterComment)

@router.message(AdmStates.EnterComment)
async def EnterComment(message: Message, state: FSMContext):
    apll = rjApl[message.from_user.id]
    if len(apll) != 0:
        apl = apll[0]
        await DBfunc.UPDATEWHERE('lcaplications', f'status = "rejected", comment = "{message.text}"', f'id = {apl[0]}')
        UserData = await DBfunc.SELECT('*', 'student', f'id = {apl[1]}')  # Запрашиваем данные пользователя
        UserData = UserData[0]
        try:
            await bot.send_message(chat_id=UserData[3],
                                   text=f'Здравствуйте {UserData[2]}. Ваше заявление №{apl[0]} Отклонено.\n'
                                        f'По причине: {message.text}')  # Отправляем ему уведомление
        except:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Бот заблокирован пользователем!')  # Если боту не удалось отправить сообщение
    else:
        await message.answer('По вашему запросу ничего не найдено.')

    if len(apll) != 1:
        apl = await DBfunc.SELECT('*', 'lcaplications', f'status = "processed"')  # Запрашиваем все заявки по статусу
        apl = apl[0]
        funcReturn = await SearchUserDataAtApl(apl)  # Получаем данные пользователя
        await bot.send_message(chat_id=message.from_user.id,
                                    text=f'AplicationID: {apl[0]}\n'
                                         f'ФИО: {funcReturn[0][2]}\n'
                                         f'Класс: {funcReturn[1]}\n'
                                         f'О себе:\n{apl[2]}',
                                    reply_markup=ViewOutputOfferInline(funcReturn[0][3]))  # Выводим новую заявку
    else:
        await bot.send_message(chat_id=message.from_user.id,
                                    text=f'Список закончился')



