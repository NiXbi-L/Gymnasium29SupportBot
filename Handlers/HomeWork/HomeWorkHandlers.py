from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(F.text == 'Домашнее задание')
async def HomeWork(messge: Message, state: FSMContext):
    await messge.answer('На какой день вы хотите посмотреть Домашнее Задание?')