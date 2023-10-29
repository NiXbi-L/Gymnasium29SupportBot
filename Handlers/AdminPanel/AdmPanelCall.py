from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from DB import DBfunc
from Handlers.States import AdmStates
from Handlers.builders import mainKeyboard, admKeyboard, ViewOutputInline
from Handlers.AdminPanel import Functions, ViewErrorReports, ViewLCRequest, ViewLCWReqest, Setings


router = Router()
router.include_routers(
    ViewLCWReqest.router,
    ViewLCRequest.router,
    Setings.router
)


@router.message(Command('adm'))
async def admPanelCall(message: Message, state: FSMContext):
    if await DBfunc.IF('adm','id',f'TelegramID = {message.from_user.id}'): #Если пользователь числится как администратор
        await message.answer('Что хотите сделать?',
                             reply_markup=admKeyboard())
        await state.set_state(AdmStates.Choice)


