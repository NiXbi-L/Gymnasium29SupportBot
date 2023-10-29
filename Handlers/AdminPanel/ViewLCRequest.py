from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery


from DB import DBfunc
from Handlers.States import AdmStates, ViewRequest
from Handlers.builders import mainKeyboard, admKeyboard, ViewOutputIdeaInline
from config import BotSetings
from Handlers.AdminPanel.Functions import SearchUserDataAtApl, sendNewRequest

router = Router()
bot = Bot(token=BotSetings.token)

rjApl = {}

@router.message(lambda message: message.text == 'Предложения по МП', AdmStates.Choice)
async def LCRequest(message: Message, state: FSMContext):
    await message.answer('Загрузка...', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
    await sendNewRequest(message.from_user.id, state,)

@router.callback_query(lambda query: query.data.startswith('Reject_'), ViewRequest.View)
async def View(call: CallbackQuery, state: FSMContext):
    id = int(call.data.split('_')[1])
    await DBfunc.UPDATEWHERE('lcidea','status = "rejected"',f'id = {id}')
    await sendNewRequest(call.from_user.id, state, 1, call.message.message_id)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
@router.callback_query(lambda query: query.data.startswith('Aprove_'), ViewRequest.View)
async def View(call: CallbackQuery, state: FSMContext):
    id = int(call.data.split('_')[1])
    await DBfunc.UPDATEWHERE('lcidea', 'status = "approved"', f'id = {id}')
    await sendNewRequest(call.from_user.id, state, 1, call.message.message_id)
    await bot.delete_message(chat_id=call.from_user.id,message_id=call.message.message_id)
