from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton
def studTeachInline():
    builder = InlineKeyboardBuilder()  # Создаем объект builder
    builder.add(
        InlineKeyboardButton(
            text="Учитель",
            callback_data='Choice_teacher'
        ),
        InlineKeyboardButton(
            text="Ученик",
            callback_data='Choice_student'
        )
    )
    return builder
def regYesNoInline(message):
    builder = InlineKeyboardBuilder()  # Создаем объект builder
    builder.add(
        InlineKeyboardButton(
            text="Нет",
            callback_data=f'Confirm_no_{message}'
        ),
        InlineKeyboardButton(
            text="Да",
            callback_data=f'Confirm_yes_{message}'
        )
    )
    return builder

def regYesNoTInline(message):
    builder = InlineKeyboardBuilder()  # Создаем объект builder
    builder.add(
        InlineKeyboardButton(
            text="Нет",
            callback_data=f'ConfirmT_no_{message}'
        ),
        InlineKeyboardButton(
            text="Да",
            callback_data=f'ConfirmT_yes_{message}'
        )
    )
    return builder

def undoInline():
    builder = InlineKeyboardBuilder()  # Создаем объект builder
    builder.add(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=f'undo'
        )
    )
    return builder

def mainKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Домашнее задание'),
        KeyboardButton(text='Расписание'),
        KeyboardButton(text='Лидер-Клуб'),
        KeyboardButton(text='Сообщить об ощибке'),
        KeyboardButton(text='Маркет'),
        KeyboardButton(text='Настройки')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def LCKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Подать заявку в Лидер-Клуб'),
        KeyboardButton(text='Предложить идею')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def LCKeyboardR():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Подать заявку в Лидер-Клуб'),
        KeyboardButton(text='Предложить идею')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
