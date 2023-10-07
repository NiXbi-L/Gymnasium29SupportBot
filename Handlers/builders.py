from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
def studTeachInline():
    builder = InlineKeyboardBuilder()  # Создаем объект builder
    builder.add(
        types.InlineKeyboardButton(
            text="Учитель",
            callback_data='Choice_teacher'
        ),
        types.InlineKeyboardButton(
            text="Ученик",
            callback_data='Choice_student'
        )
    )
    return builder
def regYesNoInline(message):
    builder = InlineKeyboardBuilder()  # Создаем объект builder
    builder.add(
        types.InlineKeyboardButton(
            text="Нет",
            callback_data=f'Confirm_no_{message}'
        ),
        types.InlineKeyboardButton(
            text="Да",
            callback_data=f'Confirm_yes_{message}'
        )
    )
    return builder

def regYesNoTInline(message):
    builder = InlineKeyboardBuilder()  # Создаем объект builder
    builder.add(
        types.InlineKeyboardButton(
            text="Нет",
            callback_data=f'ConfirmT_no_{message}'
        ),
        types.InlineKeyboardButton(
            text="Да",
            callback_data=f'ConfirmT_yes_{message}'
        )
    )
    return builder