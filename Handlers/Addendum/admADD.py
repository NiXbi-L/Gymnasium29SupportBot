from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DB import DBfunc
from DB.Hashfunc import generate_unique_key
from Handlers.States import admADDStates
from Handlers.builders import undoInline
from config import BotSetings

router = Router() #Создаем объект роутер
bot = Bot(token=BotSetings.token) #Создаем объект бот

@router.message(Command('addTeach')) #Обработчик команды addTeach
async def addTeach(message: Message, state: FSMContext):
    if await DBfunc.IF('adm', '`FSc`',
                       f'TelegramID = {message.from_user.id}'):  # Условие наличия TelegramID в таблице администраторов
        await message.answer('Введите ФИО учителя',reply_markup=undoInline().as_markup())
        await state.set_state(admADDStates.EnterFSc) # Меняем состояние на admADDStates.EnterFSc

@router.message(admADDStates.EnterFSc) #Обработчик состояния admADDStates.EnterFSc
async def EnterFSc(message: Message,state: FSMContext):
    try:
        await DBfunc.INSERT('teacher', 'FSc,`userkey`',
                            f'"{message.text}","{await generate_unique_key()}"')  # Добавляем пользователя в БД
        await state.clear() #отчищаем сосотяние
        await message.answer(f'Учитель создан\nkey:```{await generate_unique_key()}```', parse_mode="MarkdownV2")
    except Exception as e:
        print(e)
        await message.answer('Incorrect Value') #Выводим сообшение об ощибке

@router.message(Command('addStud'))
async def addStud(message: Message, state: FSMContext):
    if DBfunc.IF('adm', '`id`',
                 f'TelegramID = {message.from_user.id}'):  # Условие наличия TelegramID в таблице администраторов
        await message.answer('Введите данные в следующем формате:\n'
                             'ФИО_Класс',reply_markup=undoInline().as_markup())
        await state.set_state(admADDStates.EnterData) #Устанавливаем состояние EnterData

@router.message(admADDStates.EnterData) # Обработчик состояния EnterData
async def EnterData(message: Message, state: FSMContext):
    data = message.text.split('_') #Парсим введенные данные
    if await DBfunc.IF('class', '`id`', f'`ClassName` = "{data[1]}"'):  # Если имя класса существует
        classID = await DBfunc.SELECT('`id`', 'class', f'`ClassName` = "{data[1]}"')  # Получаем ClassID
        classID = classID[0][0]
        await DBfunc.INSERT('student', '`ClassID`,`FSc`,`user key`',
                            f'"{classID}","{data[0]}","{await generate_unique_key()}"')  # Добавляем пользователя в БД
        await message.answer(f'Ученик создан\nkey: ```{await generate_unique_key()}```',parse_mode="MarkdownV2")
        await state.clear() #Отчищаем состояние
    else:
        await message.answer('Такого класса не существует',reply_markup=undoInline().as_markup())

@router.callback_query(admADDStates.EnterData)
async def EnterData(message: Message,call: types.CallbackQuery,state: FSMContext):
    if call.data == 'undo':
        await state.clear()
        await call.answer('Действие отменено')

