from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from DB import DBfunc
from Handlers.States import LeaderClubStates
from Handlers.builders import LCKeyboard, mainKeyboard, LCKeyboardR
from Handlers.LeaderClub import LCAplications,LCWorkOffer

router = Router()
router.include_routers(
    LCAplications.router,
    LCWorkOffer.router
)

@router.message(F.text == 'Лидер-Клуб')
async def LeaderClub(message: Message, state: FSMContext):
    if await DBfunc.IF('student', '`TelegramID`', f'`TelegramID` = {message.from_user.id}'):
        if await DBfunc.IF('student', 'id', f'LeaderClub = 1'):
            await state.set_state(LeaderClubStates.Choice)
            await message.answer('Что хочешь сделать?',
                                reply_markup=LCKeyboardR())

        else:
            await state.set_state(LeaderClubStates.Choice)
            await message.answer('Что хочешь сделать?',
                                reply_markup=LCKeyboard())

@router.message(F.text == 'Назад')
async def back(message: Message, state: FSMContext):
    if await DBfunc.IF('student', '`TelegramID`', f'`TelegramID` = {message.from_user.id}'):
        await state.clear()
        await message.answer('Чем могу быть полезен?',
                             reply_markup=mainKeyboard())
