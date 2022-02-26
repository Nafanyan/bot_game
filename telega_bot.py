from aiogram.utils import executor
from create_bot import dp
from aiogram import types, Dispatcher

from handlers import sweet_game_head

sweet_game_head.registers_handlers_sweet(dp)

dp.register_message_handler(start_sweet, commands=['play_sweet'],state = None)


print('Online')
executor.start_polling(dp,skip_updates=True)