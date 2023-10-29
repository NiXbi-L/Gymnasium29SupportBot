from DB import DBfunc
from aiogram import Bot
from aiogram.types import InputMediaPhoto

from config import BotSetings
from Handlers.builders import ViewOutputOfferInline, ViewOutputIdeaInline, admKeyboard
from Handlers.States import AdmStates, ViewRequest
bot = Bot(token=BotSetings.token)

async def sedERRORtoAdm(arr,userid):
    userData = await DBfunc.SELECT('FSc,ClassID','student',f'TelegramID = {userid}')
    userData = userData[0]
    Class = await DBfunc.SELECT('ClassName','class',f'id = {userData[1]}')
    Class = Class[0][0]
    admins = await DBfunc.SELECT('TelegramID','adm',f'ErrorReprort = 1')
    media = []
    for i in range(1,len(arr[1::])+1):
        if i == 1:
            media.append(InputMediaPhoto(media=arr[i], caption=f'ФИО: {userData[0]}\n'
                                                           f'Касс: {Class}\n'
                                                           f'Описание ошибки: \n{arr[0]}'))
        else:
            media.append(InputMediaPhoto(media=arr[i]))
    for i in admins:
        await bot.send_media_group(media=media, chat_id=i[0])