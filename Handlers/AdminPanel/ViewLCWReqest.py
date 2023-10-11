from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from DB import DBfunc
from Handlers.States import AdmStates
from Handlers.builders import mainKeyboard, admKeyboard, LCAplKeyboard, ViewOutputInline
from config import BotSetings

router = Router()
bot = Bot(token=BotSetings.token)

LCaplications = {}
LCaplicationsCounter = {}

@router.message(AdmStates.Choice)
@router.message(F.data == 'Заявки в ЛК')
async def Choice(message: Message, state: FSMContext):
    await message.answer('Какие завяки вы хотите посмотреть?',
                         reply_markup=LCAplKeyboard())
    await state.set_state(AdmStates.LCAplChoice)

@router.message(AdmStates.LCAplChoice)
async def LCAplChoice(message: Message, state: FSMContext):
    LCaplications[message.from_user.id] = DBfunc.SELECT('*','lcaplications',f'status = "{message.text}"') #Запрашиваем все заявки по статусу
    if len(list(LCaplications[message.from_user.id])) != 0:
        await message.answer('Загрузка...', reply_markup=ReplyKeyboardRemove())  # Отправляем сообщение для удаления клавиатуры
        LCaplicationsCounter[message.from_user.id] = 0
        apl = LCaplications[message.from_user.id][
            LCaplicationsCounter[message.from_user.id]
        ]
        userData = DBfunc.SELECT('id,ClassID,FSc','student',f'id = {apl[1]}')[0] #Получаем данные пользователя по ID из заявки
        Class = DBfunc.SELECT('ClassName','class',f'id = {userData[1]}')[0][0] #Получаем класс в котором обучается пользователь
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=message.message_id+1) #Удаляем сообщение
        await message.answer(f'AplicationID: {apl[0]}\n'
                             f'ФИО: {userData[2]}\n'
                             f'Класс: {Class}\n'
                             f'О себе:\n{apl[2]}',
                             reply_markup=ViewOutputInline(message.from_user.id))
    else:
        await message.answer('По вашему запросу ничего не найдено',
                             reply_markup=admKeyboard())
        await state.set_state(AdmStates.Choice)

@router.callback_query(F.data.startswith("Aprove_"))
async def Aprove(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1::]
    apl = LCaplications[data[0]][
        LCaplicationsCounter[data[0]]
    ]
    DBfunc.UPDATEWHERE('lcaplications','status = "aproved"',f'id = {apl[0]}')

