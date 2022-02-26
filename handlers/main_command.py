from aiogram import types
from bot_game import storage_users as su
from bot_game import work_status_users as wsu

async def start(message : types.Message):
    id = str(message.from_user.id)
    action_info = ''
    user_base = su.read_storage()
    if (not (id in user_base)):
        su.add_new_user(id)
        wsu.new_user_status(id)
    user_base = su.read_storage()
    for action in user_base[id]:
        action_info += f'{action} \n'
    await message.answer('Привет! \n'
                             'Вот список доступных для тебя команд \n'
                             f'{action_info}')

