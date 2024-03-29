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
        #KeyboardButton(text='Маркет'),
        KeyboardButton(text='Настройки')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def LCKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Подать заявку в Лидер-Клуб'),
        KeyboardButton(text='Предложить идею'),
        KeyboardButton(text='Мероприятия'),
        KeyboardButton(text='Назад')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def LCKeyboardR():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Предложить идею'),
        KeyboardButton(text='Мероприятия'),
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
        KeyboardButton(text='Настройки'),
        KeyboardButton(text='Добавить запись'),
        KeyboardButton(text='Начать чат'),
        KeyboardButton(text='Планер'),
        KeyboardButton(text='Выйти')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def admAddKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Ученика'),
        KeyboardButton(text='Учителя'),
        KeyboardButton(text='Класса')
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

def ViewOutputOfferInline(id):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Отклонить',
            callback_data=f'Reject_{id}'
        ),
        InlineKeyboardButton(
            text='Одобрить',
            callback_data=f'Aprove_{id}'
        )
    )
    return builder.as_markup()

def ViewOutputIdeaInline(id):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Отклонить',
            callback_data=f'Reject_{id}'
        ),
        InlineKeyboardButton(
            text='Одобрить',
            callback_data=f'Aprove_{id}'
        )
    )
    return builder.as_markup()

def admSetingsKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Уведомления'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def admSetingsInline(butons):
    builder = InlineKeyboardBuilder()
    for i in butons:
        builder.add(
            InlineKeyboardButton(
                text= i,
                callback_data=f'notification_{i}'
            )
        )
    builder.adjust(2)
    return builder.as_markup()

def EnterDBKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Учитель'),
        KeyboardButton(text='Ученик'),
        KeyboardButton(text='Класс'),
        KeyboardButton(text='Назад')
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def ViewingFScInline(FSc):
    builder = InlineKeyboardBuilder()
    for i in FSc:
        builder.add(
            InlineKeyboardButton(
                text=i[0],
                callback_data=f'Teacher_{i[0]}'
            )
        )
    builder.adjust(1)
    return builder.as_markup()
def ViewingFScStudInline(FSc):
    builder = InlineKeyboardBuilder()
    for i in FSc:
        builder.add(
            InlineKeyboardButton(
                text=i,
                callback_data=f'Stud_{i}'
            )
        )
    builder.adjust(1)
    return builder.as_markup()

def PlanerKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Мероприятие'),
        KeyboardButton(text='Собрание'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def planerYesNo():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Изменить',
            callback_data=f'change'
        ),
        InlineKeyboardButton(
            text='Запланировать',
            callback_data=f'Schedule'
        )
    )
    builder.adjust(2)
    return builder.as_markup()

def planerChange():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Дату',
            callback_data=f'Date'
        ),
        InlineKeyboardButton(
            text='Название',
            callback_data=f'Name'
        ),
        InlineKeyboardButton(
            text='Описание',
            callback_data=f'Text'
        ),
        InlineKeyboardButton(
            text='Отмена',
            callback_data=f'und'
        )
    )
    builder.adjust(2)
    return builder.as_markup()

def ViewEventKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Ближайшие 30 дней'),
        KeyboardButton(text='Выбрать месяц'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def viewNameAndID(nameAndID,bl=1,Month=0):
    builder = InlineKeyboardBuilder()
    if bl:
        for i in nameAndID:
            builder.add(
                InlineKeyboardButton(
                    text=i[1],
                    callback_data=f'Event_{i[0]}_{Month}'
                )
            )
    else:
        for i in nameAndID:
            builder.add(
                InlineKeyboardButton(
                    text=i[1],
                    callback_data=f'Event_{i[0]}_{0}'
                )
            )
    builder.adjust(1)
    return builder.as_markup()

def viewNameAndIDund(Month):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f'und_{Month}'
        )
    )
    builder.adjust(1)
    return builder.as_markup()


