import asyncio
import logging

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_media_photo import InputMediaType
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Handlers.States import logSates
from DB import DBfunc

router = Router()

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
        text="Учитель",
        callback_data='teacher'
        ),
        types.InlineKeyboardButton(
            text="Ученик",
            callback_data='student'
        )
    )
    await message.answer('dev test v0.1',reply_markup=builder.as_markup())

@router.message(logSates.EnterId)
async def ceckid(message: Message, state: FSMContext):
    try:
        if DBfunc.IF('student','*',f'id = {int(message.text)} AND TelegramID != {message.from_user.id}'):
            DBfunc.UPDATE('student',f'TelegramID = {message.from_user.id}',int(message.text))
        else:
            message.answer('Incorrect ID or User in DB.')
    except:
        message.answer('Incorrect value. Try again')
