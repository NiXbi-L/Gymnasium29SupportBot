from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


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
        KeyboardButton(text='Сообщить об ошибке'),
        KeyboardButton(text='Маркет'),
        KeyboardButton(text='Настройки')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def LCKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Подать заявку в Лидер-Клуб'),
        KeyboardButton(text='Предложить идею'),
        KeyboardButton(text='Назад')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def LCKeyboardR():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Предложить идею'),
        KeyboardButton(text='Назад')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def ERRORPhotosInline(id):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='Нажать после отправки фотографий',
            callback_data=f'AddPhoto_{id}'
        ),
        InlineKeyboardButton(
            text='Продолжить без фотографий',
            callback_data=f'NoPhoto_{id}'
        )
    )
    builder.adjust(1)

    return builder.as_markup()


def admKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Заявки в ЛК'),
        KeyboardButton(text='Предложения по МП'),
        KeyboardButton(text='Сообщения об ошибках'),
        KeyboardButton(text='Настроить Маркет'),
        KeyboardButton(text='Настроить уведомления'),
        KeyboardButton(text='Выйти')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def LCAplKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='processed'),
        KeyboardButton(text='aproved'),
        KeyboardButton(text='rejected'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def ViewOutputInline(id):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Отклонить',
            callback_data=f'Aprove_{id}'
        ),
        InlineKeyboardButton(
            text='Одобрить',
            callback_data=f'Reject_{id}'
        )
    )

    builder.row(
        InlineKeyboardButton(
            text='⬅️',
            callback_data=f'Back_{id}'
        ),InlineKeyboardButton(
            text='Отмена',
            callback_data=f'Undo_{id}'
        ),
        InlineKeyboardButton(
            text='➡️',
            callback_data=f'Next_{id}'
        )
    )
    return builder.as_markup()

