from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from config import TOKEN
from db import BotDB
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging 
import time 


logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
storage = MemoryStorage()
bot = Bot(token=TOKEN)
database = BotDB('probka.db')
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer('Я-бот Пробки, созданный для того чтобы помочь тебе принять участие конкурсе.'
                        'Просто следуй моим инструкциям и все будет ОК. Для начала введи команду /start\n'
                        'Если я сломаюсь, напиши ребятам из @probka_shop33')



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    tg_id = message.from_user.id
    if database.user_exists_tg(tg_id):
            await bot.send_message(message.chat.id, 'Ты уже учавствуешь! Потерпи.')
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        reg_button = types.KeyboardButton(text="📱 Отправить", request_contact=True)
        keyboard.add(reg_button)
        await message.answer(text='Привет!\nПоделись своим номером телефона.\n'
                             'Так я буду знать, что код, который тебе дали в магазине, принадлежит тебе', reply_markup=keyboard)
    


@dp.message_handler(commands=['condition'])
async def giveaway_conditions(message: types.Message):
    await bot.send_message(message.chat.id, 'Условия конкурса:\n'
                           'Покупай в Пробке на сумму от 1000 рублей,\n'
                           'Получай уникальный шестизначный код и напиши его мне\n'
                           'Подпишись на наш телеграм-канал.\n'
                           'Всё! ')


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message, state:FSMContext):
    if message.contact is not None:
        phone_num = message.contact['phone_number']
        keyboard = types.ReplyKeyboardRemove()
        if not database.user_exists_phone(phone_num):
            await bot.send_message(message.chat.id, 'Извини, твоего номера нет в базе.\n'
                                   'Для начала тебе нужно купить пива в Пробке на 700+ рублей.'
                                   'Возвращайся, когда выполнишь это условие :)', reply_markup=keyboard)
        else:
            await state.update_data(
                {'phone_num': phone_num}
                )
            await message.answer(f'Cпасибо! Номер {phone_num} успешно отправлен', reply_markup=keyboard)
            await bot.send_message(message.chat.id, 'Теперь отправь мне шестизначный код, полученный в Пробке.')
    else:
        await bot.send_message(message.chat.id, 'Извини, но без номера я не смогу проверить, учавствуешь ли ты в конкурсе. ')
    




    
@dp.message_handler(regexp=r'^[0-9]{5,6}$')
async def id_code(message: types.Message, state: FSMContext):
    data =  await state.get_data()
    phone_num = data.get('phone_num')
    id_code = message.text
    db_id_code = str(database.get_id_code(phone_num))
    tg_id = message.from_user.id
    nickname = message.from_user.username
    if id_code == db_id_code:
        
        try:
            await bot.send_message(message.chat.id, 'Проверяю...')
            database.add_nickname(nickname, phone_num)
            database.add_tg_id(tg_id, phone_num)
            await bot.send_message(message.chat.id, 'Отлично, все получилось. Теперь жди итогов розыгрыша.')
            await state.finish()
        except Exception as e:
            await bot.send_message(message.chat.id, f'Упс, кажется что-то пошло не так((( {e}')
    else:
        await bot.send_message(message.chat.id, f'Для номера {phone_num} в моей базе другой код. Попробуй еще раз.')
    
@dp.message_handler(commands=['allusers'])
async def all_users(message: types.Message):

    users = database.all_users()
    await bot.send_message(message.chat.id, f'Список номеров всех участников: {users}')        


@dp.message_handler(content_types='any')
async def any_else(message: types.Message):
    await bot.send_message(message.chat.id, 'Что-то я тебя не понимаю.')



if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        time.sleep(3)
        print(e)


