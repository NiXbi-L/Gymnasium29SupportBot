from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from DB import DBfunc
from Handlers.States import AdmStates, Planer
from Handlers.builders import mainKeyboard, PlanerKeyboard
from Handlers.Planer import addEvent, ViewEvents

from datetime import datetime



router = Router()
router.include_routers(
    addEvent.router,
    ViewEvents.router
)

@router.message(lambda message: message.text == 'Планер', AdmStates.Choice)
async def startPlaer(message: Message, state: FSMContext):
    await message.answer('Что хотите запланировать?',reply_markup=PlanerKeyboard())
    await state.set_state(Planer.Choice)








