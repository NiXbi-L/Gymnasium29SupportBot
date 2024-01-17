from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DB import DBfunc
from Handlers.States import logSates
from Handlers.builders import studTeachInline, regYesNoInline, regYesNoTInline, mainKeyboard
from config import BotSetings

router = Router() #Создаем объект роутер
bot = Bot(token=BotSetings.token) #Создаем объект бот

@router.message(Command('start')) #Обработчик команды старт
async def start(message: Message, state: FSMContext):
    await state.clear()  # Отчищаем состояние
    if await DBfunc.IF('student','`TelegramID`',f'`TelegramID` = {message.from_user.id}'): #Если пользователь авторизован как ученик
        data = await DBfunc.SELECT('`FSc`','student',f'`TelegramID` = {message.from_user.id}')#Полуаем данные из БД
        data = data[0][0]
        await message.answer(f'Привет {data.split()[1]}. Чем могу быть полезен?',reply_markup=mainKeyboard())

    elif await DBfunc.IF('teacher','`TelegramID`',f'`TelegramID` = {message.from_user.id}'):#Если пользователь авторизован как учитель
        data = await DBfunc.SELECT('`FSc`','teacher',f'`TelegramID` = {message.from_user.id}') #Полуаем данные из БД
        data = data[0][0]
        await message.answer(f'Привет {data.split()[1]}. Чем могу быть полезен?',reply_markup=mainKeyboard())

    else: #Если пользователь на авторизован
        builder = studTeachInline() #Создаем объект builder
        await message.answer('Приветсвтую. Выберите Способ авторизации\ndev test v0.1',reply_markup=builder.as_markup()) #Выводим сообщение с инлайн кнопками

@router.message(logSates.EnterId) #Обработчик события состояния logSates.EnterId
async def ceckid(message: Message, state: FSMContext):
    try:
        if await DBfunc.IF('student','*', f'`user key` = "{message.text}" AND TelegramID != {message.from_user.id}'): #Проверяем через БД условие если key указан верно и TelegramID != UserTelegramID
            FSc = await DBfunc.SELECT('`id`,`FSc`','student',f'`user key` = "{message.text}"') #Получаем ФИО и id пользователя по ввведенному ключу
            FSc = FSc[0]
            await message.answer(f'Вы {FSc[1]}?', reply_markup=regYesNoInline(FSc[0]).as_markup())#Отпавляем сообщение о подтверждении
        else:
            await message.answer('Incorrect ID or User in DB.') #Выводим сообщение об ошибке о неверно введенных данных или пользователь уже в системе
    except Exception as e:
        print(e)
        await message.answer('Incorrect value. Try again') #Выводим сообщение об ошибке данных

@router.message(logSates.EnterIdT) #Обработчик события состояния logSates.EnterIdT
async def ceckid(message: Message, state: FSMContext):
    try:
        if await DBfunc.IF('teacher','*',f'`userkey` = "{message.text}" AND TelegramID != {message.from_user.id}'): #Проверяем через БД условие если key указан верно и TelegramID != UserTelegramID
            FSc = await DBfunc.SELECT('`id`,`FSc`','teacher',f'`userkey` = "{message.text}"') # получаем ФИО и id пользователя по ключу
            Sc = FSc[0]
            await message.answer(f'Вы {FSc[1]}?',reply_markup=regYesNoTInline(FSc[0]).as_markup())
        else:
            await message.answer('Некорректный ID') #Выводим сообщение об ошибке о неверно введенных данных или пользователь уже в системе
    except Exception as e:
        if BotSetings.Debug:
            print(e)
            await bot.send_message(chat_id=BotSetings.admin,
                                   text=f'ERROR\n '
                                        f'User: {message.from_user.username}\n '
                                        f'id: {message.from_user.id}\n '
                                        f'Eerror log: {e}') #Отправляем сообщение об ошибке гл. адмигисьоаьлоу
        await message.answer('Incorrect value. Try again') #Выводим сообщение об ошибке данных



@router.callback_query(F.data.startswith("Choice_")) #Обработчик колбеков выбора
async def Choice(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1]  # Убераем тег из call.data
    if data == 'teacher':
        await state.set_state(logSates.EnterIdT)  # Меняем состояние на logSates.EnterIdT
    if data == 'student':
        await state.set_state(logSates.EnterId)  # Меняем состояние на logSates.EnterId
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Enter key')  #Редактируем сообщение с кнопками и просим пользователя ввести ключь

@router.callback_query(F.data.startswith("Confirm_"))#Подтверждение Ученик
async def Confirm(call: types.callback_query, state: FSMContext):
    data = call.data.split("_")[1]  # Убераем тег из call.data
    messageText = call.data.split("_")[2]  # Достаем MessageText из data
    if data == 'yes':
        await DBfunc.UPDATEWHERE('student', f'TelegramID = {call.from_user.id}',
                               f'`id` = {messageText}')  # Обновляем поле TelegramID на TelegramID пользователя
        await bot.delete_message(message_id=call.message.message_id, chat_id=call.from_user.id)
        await bot.send_message(chat_id=call.from_user.id,
                                        text='Ваш TelegramID верифицирован. Приятного пользования!',
                                        reply_markup=mainKeyboard())  # Редактируем сообщение с кнопками и просим пользователя ввести ключь
        await state.clear()
    if data == 'no':
        builder = studTeachInline()  # Создем объект builder
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                        text='dev test v0.1',
                                        reply_markup=builder.as_markup())  # Редактируем сообщение с кнопками и просим пользователя ввести ключь
        await state.set_state(logSates.Choice)

@router.callback_query(F.data.startswith("ConfirmT_"))#Подтверждение Учитель
async def Confirm(call: types.callback_query, state: FSMContext):
    data = call.data.split("_")[1]  # Убераем тег из call.data
    messageText = call.data.split("_")[2]  # Достаем MessageText из data
    if data == 'yes':
        await DBfunc.UPDATEWHERE('teacher', f'TelegramID = {call.from_user.id}',
                               f'`id` = "{messageText}"')  # Обновляем поле TelegramID на TelegramID пользователя
        await bot.delete_message(message_id=call.message.message_id, chat_id=call.from_user.id)
        await bot.send_message(chat_id=call.from_user.id,
                                        text='Ваш TelegramID верифицирован. Приятного пользования!',
                                        reply_markup=mainKeyboard())  # Редактируем сообщение с кнопками и выводим сообщение об успешной регистрации
        await state.clear()
    if data == 'no':
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                        text='Приветсвтую. Выберите Способ авторизации\ndev test v0.1 ',
                                        reply_markup=studTeachInline().as_markup())  # Редактируем сообщение с кнопками и просим пользователя ввести ключь
        await state.set_state(logSates.Choice)
