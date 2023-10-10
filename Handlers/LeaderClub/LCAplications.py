from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,ReplyKeyboardRemove

from Handlers.States import LeaderClubStates
from Handlers.builders import mainKeyboard
from DB import DBfunc

router = Router()

@router.message(F.text == 'Предложить идею')
async def idea(message: Message, state: FSMContext):
    await state.set_state(LeaderClubStates.EnterIdea)
    await message.answer('Напиши что ты хочешь предложить. (Max 300 символов)',
                         reply_markup=ReplyKeyboardRemove())

@router.message(LeaderClubStates.EnterIdea)
async def EnterIdea(message: Message, state: FSMContext):
    if len(list(message.text)) <= 300:
        userid = DBfunc.SELECT('id', 'student', f'TelegramID = {message.from_user.id}')[0][0]
        if DBfunc.COUNT('lcidea','id',f'userid = {userid}') < 1:
            DBfunc.INSERT('lcidea','userid,text',f'{userid},"{message.text}"') #Создаем запись о заявке пользователя
            await message.answer('Ваша заявка отправлена!',
                                 reply_markup=mainKeyboard())
            await state.clear()

        else:
            await message.answer('У вас уже есть активная заявка',
                                 reply_markup=mainKeyboard())
            await state.clear()
    else:
        await message.answer(f'Ваше сообщение выходит за лимит в 300 символов:\n```{message.text[300::]}```\nПопробуйте еще раз',parse_mode="MarkdownV2")