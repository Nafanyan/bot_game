from bot_game.algoritms import sweet_game_algo
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_game import work_status_users as wsu


total_sweets = 45
max_sweet = 6


class stage_sweet(StatesGroup):
    choice = State()
    now_game = State()
    end_game = State()

async def start_sweet(message : types.Message):
    id = message.from_user.id
    last_value = int(wsu.read_status(id)['play_sweet'][0])
    if (last_value != total_sweets and last_value != 0):
        await message.answer(f'Ухты, у тебя есть незаконченная игра где осталось ещё {last_value} конфет/ы. \n'
                             f'Надо её закончить, кто будет ходить первым, Я или Ты?')
        sweet_game_algo.init_sweet(last_value, max_sweet)
    else:
        sweet_game_algo.init_sweet(total_sweets, max_sweet)
        await message.answer(f'Правила игры!\n'
                             f'1. Всего {total_sweets} конфет, брать можешь не больше {max_sweet}\n'
                             f'2. Ходим по очереди\n'
                             f'3. Кто последний берет конфеты тот и победил.\n'
                             f'Кто будет ходить первым, Я или Ты?')
    await stage_sweet.choice.set()

async def chouse_step(message : types.Message, state : stage_sweet):

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
    try:
        id = message.from_user.id
        num = int(message.text)
        winner = True
        if (sweet_game_algo.check(num)):
            sweet_game_algo.player_step(num)
        else:
            await message.answer(f'Ты не можешь взять такое количество конфет')
            await stage_sweet.now_game.set()
        if (sweet_game_algo.remained_sweet() != 0 and sweet_game_algo.check(num)):
            await message.answer(f'Осталось {sweet_game_algo.remained_sweet()}')
            await message.answer(f'Я взял {sweet_game_algo.bot_step()}\nОсталось {sweet_game_algo.remained_sweet()}')
            winner = False

        new_status = wsu.read_status(id)
        if (sweet_game_algo.remained_sweet() > 0):
            await stage_sweet.now_game.set()
            new_status['play_sweet'][0] = sweet_game_algo.remained_sweet()
            wsu.change_status(new_status, id)
        else:
            if (winner):
                await message.answer('Поздравляю, победа за тобой')
            else:
                await message.answer('Увы, но победа за мной')
            await message.answer(f'Хочешь ещё раз сыграть?\n'
                                 f'Напиши "да", если хочешь, или "нет", если наигрался.')
            new_status['play_sweet'][0] = total_sweets
            wsu.change_status(new_status, id)
            await stage_sweet.end_game.set()
    except: await message.answer('Пиши ответ целым числом, пожалуйста.')





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


