from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from DB import DBfunc
from DB.Hashfunc import generate_unique_key
from Handlers.States import admADDStates, AdmStates
from Handlers.builders import undoInline, EnterDBKeyboard, admKeyboard, ViewingFScInline
from config import BotSetings

router = Router() #Создаем объект роутер
bot = Bot(token=BotSetings.token) #Создаем объект бот

ClassData = {}


@router.message(lambda message: message.text == 'Добавить запись', AdmStates.Choice)
async def EnterDB(message: Message, state: FSMContext):
    await message.answer('Какую запись хотите добавить?', reply_markup=EnterDBKeyboard())
    await state.set_state(AdmStates.EnterDB)


@router.message(lambda message: message.text == 'Учитель', AdmStates.EnterDB)  # Обработчик команды addTeach
async def addTeach(message: Message, state: FSMContext):
    await message.answer('Загрузка...', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
    await message.answer('Введите ФИО учителя', reply_markup=undoInline().as_markup())
    await state.set_state(admADDStates.EnterFSc) # Меняем состояние на admADDStates.EnterFSc

@router.message(admADDStates.EnterFSc) #Обработчик состояния admADDStates.EnterFSc
async def EnterFSc(message: Message,state: FSMContext):
    try:
        key = await generate_unique_key()
        await DBfunc.INSERT('teacher','FSc,`userkey`',
                            f'"{message.text}","{key}"')  # Добавляем пользователя в БД
        await state.clear() #отчищаем сосотяние
        await message.answer(f'Учитель создан\nkey:```{key}```', parse_mode="MarkdownV2", reply_markup= admKeyboard())
        await state.set_state(AdmStates.Choice)
    except Exception as e:
        print(e)
        await message.answer('Incorrect Value') #Выводим сообшение об ощибке


@router.message(lambda message: message.text == 'Ученик', AdmStates.EnterDB)
async def addStud(message: Message, state: FSMContext):
    await message.answer('Загрузка...', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
    await message.answer('Введите данные в следующем формате:\n'
                             'ФИО_Класс',reply_markup=undoInline().as_markup())
    await state.set_state(admADDStates.EnterData) #Устанавливаем состояние EnterData

@router.message(admADDStates.EnterData) # Обработчик состояния EnterData
async def EnterData(message: Message, state: FSMContext):
    data = message.text.split('_') #Парсим введенные данные
    if await DBfunc.IF('class', '`id`', f'`ClassName` = "{data[1]}"'):  # Если имя класса существует
        classID = await DBfunc.SELECT('`id`', 'class', f'`ClassName` = "{data[1]}"')  # Получаем ClassID
        classID = classID[0][0]
        key = await generate_unique_key()
        await DBfunc.INSERT('student', '`ClassID`,`FSc`,`user key`',
                            f'"{classID}","{data[0]}","{key}"')  # Добавляем пользователя в БД
        await message.answer(f'Ученик создан\nkey: ```{key}```',parse_mode="MarkdownV2", reply_markup= admKeyboard())
        await state.set_state(AdmStates.Choice)
    else:
        await message.answer('Такого класса не существует', reply_markup=undoInline().as_markup())


@router.message(lambda message: message.text == 'Класс', AdmStates.EnterDB)
async def Class(message: Message, state: FSMContext):
    await message.answer('Загрузка...', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
    await message.answer('Введите данные ФИО классного руководителя(Можно частично).', reply_markup=undoInline().as_markup())
    await state.set_state(admADDStates.EnterTData)  # Устанавливаем состояние EnterСData

@router.message(admADDStates.EnterTData)
async def EnterCData(message: Message, state: FSMContext):
    FSc = await DBfunc.SELECT('FSc','teacher',f'FSc LIKE "%{message.text}%"')
    if len(FSc) != 0:
        await message.answer('Вот что нашлось по вашему запросу:', reply_markup=ViewingFScInline(FSc))
        await state.set_state(admADDStates.EnterCData)

@router.callback_query(lambda query: query.data.startswith("Teacher_"), admADDStates.EnterCData)
async def EnterCData(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')[1]
    ClassData[call.from_user.id] = data
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Введите название класса')
    await state.set_state(admADDStates.EnterClassNum)

@router.message(admADDStates.EnterClassNum)
async def EnterClassNum(message: Message, state: FSMContext):
    if len(list(message.text)) <= 3:
        Tid = await DBfunc.SELECT('id','teacher',f'FSc = "{ClassData[message.from_user.id]}"')
        Tid = Tid[0][0]
        await DBfunc.INSERT('class','ClassName,ClassroomTeacherID',f'"{message.text}",{Tid}')
        await message.answer(f'Класс {message.text} создан.', reply_markup=admKeyboard())
        await state.set_state(AdmStates.Choice)
    else:
        await message.answer('Попробуйте снова')
@router.message(lambda message: message.text == 'Назад', AdmStates.EnterDB)
async def Back(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdmStates.Choice)
    await bot.send_message(chat_id=call.from_user.id, text='Что хотите сделать?', reply_markup=admKeyboard())


@router.callback_query(lambda query: query.data == 'undo', admADDStates.EnterData)
@router.callback_query(lambda query: query.data == 'undo', admADDStates.EnterFSc)
async def Back(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdmStates.Choice)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=call.from_user.id, text='Что хотите сделать?', reply_markup=admKeyboard())
