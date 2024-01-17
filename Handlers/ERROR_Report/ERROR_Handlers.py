from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, callback_query, ReplyKeyboardRemove

from DB import DBfunc
from Handlers.States import ERROR_States
from Handlers.builders import ERRORPhotosInline, mainKeyboard
from Handlers.ERROR_Report.Fuctions import sedERRORtoAdm, Hours
from config import BotSetings, KDA


from datetime import timedelta, datetime

router = Router()
bot = Bot(token=BotSetings.token)

photos = {}


@router.message(lambda message: message.text == 'Сообщить об ошибке')
async def ErrorReport(message: Message, state: FSMContext):
    if DBfunc.IF('student', '`TelegramID`', f'`TelegramID` = {message.from_user.id}'):
        userid = await DBfunc.SELECT('id','student', f'TelegramID = {message.from_user.id}')
        userid = userid[0][0]
        if not(await DBfunc.IF('error','*',f'userid = {userid} AND date >= DATE_SUB(NOW(), INTERVAL {KDA.ERROr} HOUR)')):
            await state.set_state(ERROR_States.EnterReport)
            await message.answer('Напишите с какой проблемой столкнулись.', reply_markup=ReplyKeyboardRemove())
        else:
            date = await DBfunc.SELECT('date','error',f'userid = {userid} AND date >= DATE_SUB(NOW(), INTERVAL {KDA.ERROr} HOUR)')
            date = date[0][0]
            await message.answer(f'Вы не можете отправлять отчет об ошибке еще {await Hours((KDA.ERROr * 3600 - (datetime.now()-date).total_seconds()))}')


@router.message(ERROR_States.EnterReport)
async def ERRORreport(message: Message, state: FSMContext):
    if len(list(message.text)) <= 300:
        photos[message.from_user.id] = [message.text]
        await state.set_state(ERROR_States.AddPhotos)
        await message.answer('Отправьте фотографии если они есть',
                             reply_markup=ERRORPhotosInline(message.from_user.id))


@router.message(ERROR_States.AddPhotos)
async def AddPhotos(message: Message, state: FSMContext):
    try:
        photos[message.from_user.id].append(message.photo[-1].file_id)
    except:
        await message.answer('Вы отправили не фото.')


@router.callback_query(lambda query: query.data.startswith("AddPhoto_") and len(photos[query.from_user.id]) > 1, ERROR_States.AddPhotos)
async def EnterPhotos(call: callback_query, state: FSMContext):
    useridTG = int(call.data.split('_')[1])  # Парсим из call.data TelegramID
    userid = await DBfunc.SELECT('id', 'student', f'TelegramID = {useridTG}')  # Запрашиваем userid из БД
    userid = userid[0][0]
    st = ''
    for i in photos[useridTG][1::]:  # Создаем единую строку с fileid
        st += i + '|'
    await DBfunc.INSERT('error', 'userid,text,photo',
                        f'{userid},"{photos[useridTG][0]}","{st}"')  # Создаем запись в БД о новой заявке
    await sedERRORtoAdm(photos[useridTG], call.from_user.id) #отсылаем сообщение всем админам
    photos[useridTG] = []  # Отчищаем запись в словаре о заявке
    await state.clear()  # Отчищаем состояние
    await bot.delete_message(message_id=call.message.message_id,
                             chat_id=useridTG)  # Удаляем сообщение с инлайн кнопками
    await bot.send_message(chat_id=useridTG,
                           text='Сообщение об ошибке отправлено!',
                           reply_markup=mainKeyboard())  # Возвращаем главную к лавиатуру


@router.callback_query(lambda query: query.data.startswith("NoPhoto_"), ERROR_States.AddPhotos)
async def NoPhoto(call: callback_query, state: FSMContext):
    useridTG = int(call.data.split('_')[1])  # Парсим из call.data TelegramID
    userid = await DBfunc.SELECT('id', 'student', f'TelegramID = {useridTG}')  # Запрашиваем userid из БД
    userid = userid[0][0]
    await DBfunc.INSERT('error', 'userid,text',
                        f'{userid},"{photos[useridTG][0]}"')  # Создаем запись в БД о новой заявке
    await sedERRORtoAdm(photos[useridTG], call.from_user.id)  # отсылаем сообщение всем админам
    photos[useridTG] = []  # Отчищаем запись в словаре о заявке
    await state.clear()  # Отчищаем состояние
    await bot.delete_message(message_id=call.message.message_id,
                             chat_id=useridTG)  # Удаляем сообщение с инлайн кнопками
    await bot.send_message(chat_id=useridTG,
                           text='Сообщение об ошибке отправлено!',
                           reply_markup=mainKeyboard())  # Возвращаем главную к лавиатуру
