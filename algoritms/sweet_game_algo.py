
from random import randint

# Инициализация конфет
def init_sweet (max_sweet, max_step):
    global now_sweet
    now_sweet = max_sweet
    global take_sweet
    take_sweet = max_step

#ход бота
def bot_step():

    answer = randint(1,6)
    while (not(check(answer))):
        answer = randint(1, 6)
    init_sweet(now_sweet - answer,take_sweet)
    return answer

# Ход игрока
def player_step(num):
    init_sweet(now_sweet - num,take_sweet)
    return num

# Проверка адекватности ввода пользователя
def check(num):
    return now_sweet - num >= 0 and num <= take_sweet and num > 0

# Возврат оставшихся конфет
def remained_sweet():
    return now_sweet
