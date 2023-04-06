from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from helpers import TOKEN

import openpyxl
import logging 

from db import BotDB


logging.basicConfig(filename='probka/logs.txt', level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')
logging.debug('Start')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
database = BotDB('/mnt/c/Users/Yevhenii/Documents/probka.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reg_button = types.KeyboardButton(text='Отправить номер телефона', request_contact=True)
    keyboard.add(reg_button)
    await message.answer(text='Привет!\nДля начала, поделись своим номером телефона.\n'
                         'Так я буду знать, что код, который тебе дали в магазине, принадлежит тебе', reply_markup=keyboard)
    
    


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    if message.contact is not None:
        keyboard = types.ReplyKeyboardRemove()
        await message.reply('Номер успешно отправлен', reply_markup=keyboard)
        await bot.send_message(message.chat.id, 'Теперь отправь мне шестизначный код, полученный в Пробке.')
        
 


    
@dp.message_handler(regexp=r'^[0-9]{6}$')
async def id_code(message :types.Message):
    if message.text == database.get_id_code(phone_num):
        try:
            database.add_nickname(message.from_user.username, message.text)
            await bot.send_message(message.chat.id, 'Проверяю...')
        except Exception as e:
            await bot.send_message(message.chat.id, 'Упс, кажется что-то пошло не так(((')
    else:
        await message.reply('Похоже, этот код не подходит.')





executor.start_polling(dp, skip_updates=True)