
from random import randint

# Инициализация конфет
def init_sweet (max_sweet, max_step):
    global now_sweet
    now_sweet = max_sweet
    global take_sweet
    take_sweet = max_step

#ход бота
def bot_step():
    answer = 1
    if (now_sweet <= 6): answer = now_sweet
    else:
        for i in range(1, take_sweet):
            if ((now_sweet - answer) % (take_sweet + 1) == 0):
                break
            answer = answer + 1
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


