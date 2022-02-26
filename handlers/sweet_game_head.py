from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers import sweet_game_algo

total_sweets = 45
max_sweet = 6

class stage_sweet(StatesGroup):
    choice = State()
    now_game = State()
    end_game = State()

async def start_sweet(message : types.Message):
    await stage_sweet.choice.set()
    await message.answer(f'Правила игры!\n'
                         f'1. Всего {total_sweets} конфет, брать можешь не больше {max_sweet}\n'
                         f'2. Ходим по очереди\n'
                         f'Кто будет ходить первым, Я или Ты?')

async def chouse_step(message : types.Message, state : stage_sweet):
    sweet_game_algo.init_sweet(total_sweets, max_sweet)
    if (message.text == 'Я' or message.text == 'я'):
        await message.answer('Хорошо, ходи')
        await stage_sweet.next()

    elif (message.text == 'Ты' or message.text == 'ты'):
        await message.answer('Хорошо, я первый')
        await message.answer(f'Я взял {sweet_game_algo.bot_step()}')
        await message.answer(f'Осталось {sweet_game_algo.remained_sweet()}')
        await stage_sweet.next()

    else:
        await message.answer(f'Я тебя не совсем понимаю, напиши "Я" или "Ты".')
        await stage_sweet.choice.set()


async def load_num(message : types.Message, state : stage_sweet):
    num = int(message.text)
    winner = True
    if (sweet_game_algo.check(num)):
        sweet_game_algo.player_step(num)
    else:
        await message.answer(f'Ты не можешь взять такое количество конфет')
        await stage_sweet.now_game.set()
    if(sweet_game_algo.remained_sweet() != 0 and sweet_game_algo.check(num)):
        await message.answer(f'Осталось {sweet_game_algo.remained_sweet()}')
        await message.answer(f'Я взял {sweet_game_algo.bot_step()}\n Осталось {sweet_game_algo.remained_sweet()}')
        winner = False

    if (sweet_game_algo.remained_sweet() > 0):
        await stage_sweet.now_game.set()
    else:
        if (winner): await message.answer('Поздравляю, победа за тобой')
        else: await message.answer('Увы, но победа за мной')
        await message.answer(f'Хочешь ещё раз сыграть?\n'
                             f'Напиши "да", если хочешь, или "нет", если наигрался.')
        await stage_sweet.end_game.set()



async def finish_game(message : types.Message, state : stage_sweet):
    if (message.text == 'да' or message.text == 'Да'):
        await message.answer('Отлично, кто ходит первым?')
        await stage_sweet.choice.set()
    elif(message.text == 'нет' or message.text == 'Нет'):
        await message.answer('Хорошо')
    else:
        await message.answer('Ты глупый или да?')
        await stage_sweet.end_game.set()



def registers_handlers_sweet(dp : Dispatcher):
    dp.register_message_handler(start_sweet, commands=['play_sweet'],state = None)
    dp.register_message_handler(chouse_step, state=stage_sweet.choice)
    dp.register_message_handler(load_num, state=stage_sweet.now_game)
    dp.register_message_handler(finish_game, state=stage_sweet.end_game)


