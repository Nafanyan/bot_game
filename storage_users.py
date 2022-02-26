# Модуль для работы с файлом в котором хранится id пользователя и список доступных ему команд


users_rights: dict = {}
users_actions = ['/play_sweet']

# Считать данные всех пользователей с хранилища
def read_storage():
    info = open('info_users/storage_users.txt','r')
    for data in info:
        data_list = data.split()
        list_action = []
        for i in range(1,len(data_list)):
            list_action.append(data_list[i])
        users_rights[data_list[0]] = list_action
    info.close()
    return users_rights

# Добавить нового пользователя в хранилище
def add_new_user(id):
    info = open('info_users/storage_users.txt','a')
    info.writelines(f'\n{id} ')
    for i in users_actions:
        info.writelines(f'{i} ')
    info.close()

# Добавляем к имеющимся пользователям новые функции (если будет расширение функционала)
def add_new_func(list_id):
    old_source = read_storage()
    info = open('info_users/storage_users.txt', 'w')
    sup_str = ''
    for id in old_source:
        sup_str += id
        for old_act in old_source[id]:
            sup_str += f' {old_act}'
        for new_act in list_id:
            sup_str += f' {new_act}'
        sup_str +='\n'
        info.writelines(sup_str)
        sup_str = ''
    info.close()




