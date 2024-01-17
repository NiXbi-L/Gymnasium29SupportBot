from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from DB import DBfunc
from Handlers.States import LeaderClubStates, ViewEvents
from Handlers.builders import mainKeyboard, ViewEventKeyboard, viewNameAndID, viewNameAndIDund
from config import BotSetings

router = Router()
bot = Bot(token=BotSetings.token)
month_to_number = {
    'январь': 1,
    'февраль': 2,
    'март': 3,
    'апрель': 4,
    'май': 5,
    'июнь': 6,
    'июль': 7,
    'август': 8,
    'сентябрь': 9,
    'октябрь': 10,
    'ноябрь': 11,
    'декабрь': 12
}


@router.message(lambda message: message.text == 'Мероприятия', LeaderClubStates.Choice)
async def Events(message: Message, state: FSMContext):
    await message.answer('За какой период мы хотите посмотреть мероприятия?', reply_markup=ViewEventKeyboard())
    await state.set_state(ViewEvents.Choice)


@router.message(lambda message: message.text == 'Ближайшие 30 дней', ViewEvents.Choice)
async def days(message: Message, state: FSMContext):
    nameAndID = await DBfunc.SELECT('id,name', 'eventplaner',
                                    f'date >= CURRENT_DATE AND date <= CURRENT_DATE + INTERVAL 30 DAY')
    if len(nameAndID) != 0:
        await message.answer('Загрузка...', reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
        await message.answer('Вот что нашлось по вашем запросу', reply_markup=viewNameAndID(nameAndID,0))
        await state.set_state(ViewEvents.View)
    else:
        await message.answer('По вашему запросу ничего не найдено', reply_markup=mainKeyboard())
        await state.clear()


@router.message(lambda message: message.text == 'Выбрать месяц', ViewEvents.Choice)
async def month(message: Message, state: FSMContext):
    await message.answer('Введите название месяца или его номер', reply_markup=ReplyKeyboardRemove())
    await state.set_state(ViewEvents.EnterMonth)


@router.message(ViewEvents.EnterMonth)
async def EnterMonth(message: Message, state: FSMContext):
    try:
        if int(message.text) <= 12:
            nameAndID = await DBfunc.SELECT('id,name', 'eventplaner',
                                            f'MONTH(date) = {int(message.text)}')
            if len(nameAndID) != 0:
                await message.answer('Вот что нашлось по вашем запросу',
                                     reply_markup=viewNameAndID(nameAndID,Month= int(message.text)))
                await state.set_state(ViewEvents.View)
            else:
                await message.answer('По вашему запросу ничего не найдено', reply_markup=mainKeyboard())
                await state.clear()
        else:
            await message.answer('Нет такого месяца')

    except(ValueError, TypeError):
        if message.text.lower() in list(month_to_number):
            nameAndID = await DBfunc.SELECT('id,name', 'eventplaner',
                                            f'MONTH(date) = {month_to_number[message.text.lower()]}')
            if len(nameAndID) != 0:
                await message.answer('Вот что нашлось по вашем запросу',
                                     reply_markup=viewNameAndID(nameAndID,Month= month_to_number[message.text.lower()]))
                await state.set_state(ViewEvents.View)
            else:
                await message.answer('По вашему запросу ничего не найдено', reply_markup=mainKeyboard())
                await state.clear()
        else:
            await message.answer('Нет такого месяца')


@router.callback_query(lambda query: query.data.startswith('Event_'), ViewEvents.View)
async def View(call: CallbackQuery, state: FSMContext):
    data = int(call.data.split('_')[1])
    Month = int(call.data.split('_')[2])
    eventData = await DBfunc.SELECT('*', 'eventplaner', f'id = {data}')
    eventData = eventData[0]
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text=f'Название: {eventData[1]}\n'
                                     f'Дата: {eventData[3]}\n'
                                     f'Описание:\n{eventData[2]}',
                                reply_markup=viewNameAndIDund(Month))


@router.callback_query(lambda query: query.data.startswith('und_'), ViewEvents.View)
async def und(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')[1]
    if int(data) != 0:
        nameAndID = await DBfunc.SELECT('id,name', 'eventplaner',
                                        f'MONTH(date) = {int(data)}')
        if len(nameAndID) != 0:
            await bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text='Вот что нашлось по вашему запросу',
                                        reply_markup=viewNameAndID(nameAndID, Month=data))
    else:
        nameAndID = await DBfunc.SELECT('id,name', 'eventplaner',
                                        f'date >= CURRENT_DATE AND date <= CURRENT_DATE + INTERVAL 30 DAY')
        if len(nameAndID) != 0:
            await bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text='Вот что нашлось по вашему запросу',
                                        reply_markup=viewNameAndID(nameAndID, 0))
