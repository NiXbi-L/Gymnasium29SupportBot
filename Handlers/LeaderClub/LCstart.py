from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Handlers.States import LeaderClubStates
from Handlers.builders import LCKeyboard, mainKeyboard, LCKeyboardR
from DB import DBfunc

router = Router()

@router.message(F.text == 'Лидер-Клуб')
async def LeaderClub(messge: Message, state: FSMContext):
    if DBfunc.IF('student','id',f'LeaderClub = 1'):
        await state.set_state(LeaderClubStates.Choice)
        await messge.answer('Что хочешь сделать?',
                            reply_markup=LCKeyboardR())

    else:
        await state.set_state(LeaderClubStates.Choice)
        await messge.answer('Что хочешь сделать?',
                            reply_markup=LCKeyboard())

@router.message(F.text == 'Назад')
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Чем могу быть полезен?',
                         reply_markup=mainKeyboard())