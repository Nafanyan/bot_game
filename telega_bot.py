from aiogram.utils import executor
from create_bot import dp
from handlers import sweet_game_head
from bot_game.handlers import main_command

sweet_game_head.registers_handlers_sweet(dp)

dp.register_message_handler(main_command.start, commands=['start'])


print('Online')
executor.start_polling(dp,skip_updates=True)