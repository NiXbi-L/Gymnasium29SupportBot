from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, callback_query, ReplyKeyboardRemove

from DB import DBfunc
from Handlers.States import AdmStates, Chat
from Handlers.builders import mainKeyboard, ViewingFScStudInline
from Handlers.Chat import Chating
from config import BotSetings

router = Router()
router.include_routers(Chating.router)
bot = Bot(token=BotSetings.token)




@router.message(lambda message: message.text == 'Начать чат', AdmStates.Choice)
async def StartChating(message: Message, state: FSMContext):
    await message.answer('Ведите поисковой запрос содержащий полное или частичное ФИО.', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Chat.EnterFSc)

@router.message(Chat.EnterFSc)
async def EnterFSc(message: Message, state: FSMContext):
    FSc = await DBfunc.SELECT('*', 'student', f'FSc LIKE "%{message.text}%" AND TelegramID != 0 AND TelegramID != {message.from_user.id}')
    print(f'{FSc}\n{[i[2] for i in FSc]}')
    if len(FSc) != 0:
        await message.answer('Вот что нашлось по вашему запросу:', reply_markup=ViewingFScStudInline([i[2] for i in FSc]))
        await state.set_state(Chat.Choice)
    else:
        await message.answer('По вашему запросу ничего не найдено.')



