from DB import DBfunc
from aiogram import Bot
from config import BotSetings
from Handlers.builders import ViewOutputOfferInline, ViewOutputIdeaInline, admKeyboard
from Handlers.States import AdmStates, ViewRequest
bot = Bot(token=BotSetings.token)


async def SearchUserDataAtApl(apl):
    userData = await DBfunc.SELECT('id,ClassID,FSc,TelegramID', 'student', f'id = {apl[1]}')  # Получаем данные пользователя по ID из заявки
    userData = userData[0]
    Class = await DBfunc.SELECT('ClassName', 'class', f'id = {userData[1]}') # Получаем класс в котором обучается пользователь
    return [
        userData,
        Class[0][0]
    ]
async def sendNewApl(apll,data,call):
    if len(apll) != 1:
        apl = await DBfunc.SELECT('*', 'lcaplications', f'status = "processed"') #Запрашиваем все заявки по статусу
        apl = apl[0]
        funcReturn = await SearchUserDataAtApl(apl) #Получаем данные пользователя
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=f'AplicationID: {apl[0]}\n'
                                         f'ФИО: {funcReturn[0][2]}\n'
                                         f'Класс: {funcReturn[1]}\n'
                                         f'О себе:\n{apl[2]}',
                                    reply_markup=ViewOutputOfferInline(int(data[0]))) #Выводим новую заявку
    else:
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=f'Список закончился')

async def admnotification(message, type):
    admid = await DBfunc.SELECT(f'TelegramID,{type}', 'adm', 'id != 0')
    send = 0
    sendError = 0
    for i in admid:
        if i[1]:
            try:
                await bot.send_message(chat_id=i[0], text= message)
                send += 1
            except:
                sendError +=1
                continue
    return [send, sendError]

async def genButtons(id):
    ntf = await DBfunc.SELECT('marcket,LCOffer,LCWOffer,ErrorReprort', 'adm',
                              f'TelegramID = {id}')  # Получаем данные о получении уведомлений
    ntf = ntf[0]
    buttonName = ['marcket', 'LCOffer', 'LCWOffer', 'ErrorReprort']  # Список названий кнопок
    buttons = []
    for i in range(len(buttonName)):
        if ntf[i]:  #Если уведомление включено
            buttons.append(f'Отключить {buttonName[i]}')
        else:
            buttons.append(f'Включить {buttonName[i]}')
    return buttons

async def sendNewRequest(id, state,bl=1,msg_id=0):
    requsest = await DBfunc.SELECT('*','lcidea',f'status = "processed"')
    if len(requsest) != 0:
        requsest = requsest[0]
        funcReturn = await SearchUserDataAtApl(requsest) #Получаем данные пользователя
        if bl:
            await bot.send_message(chat_id=id, text=f'AplicationID: {requsest[0]}\n'
                                             f'ФИО: {funcReturn[0][2]}\n'
                                             f'Класс: {funcReturn[1]}\n'
                                             f'Предложение:\n{requsest[2]}', reply_markup=ViewOutputIdeaInline(requsest[0]))
            await state.set_state(ViewRequest.View)
        else:
            await bot.edit_message_text(chat_id=id,message_id=msg_id, text=f'AplicationID: {requsest[0]}\n'
                                                    f'ФИО: {funcReturn[0][2]}\n'
                                                    f'Класс: {funcReturn[1]}\n'
                                                    f'Предложение:\n{requsest[2]}',
                                   reply_markup=ViewOutputIdeaInline(requsest[0]))
    else:
        if not(bl):
            await bot.send_message(chat_id=id, text='По вашему запросу ничего не найдено', reply_markup=admKeyboard())
        else:
            await bot.send_message(chat_id=id, text='Список закончился', reply_markup=admKeyboard())
        await state.set_state(AdmStates.Choice)



