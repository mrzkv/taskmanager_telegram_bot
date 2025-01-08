import re
from data_base_functions import check_group_name
# Валидация данных.
async def isvalid(command, type_of_command):
    command = str(command)
    # Проверка команды /add
    if type_of_command == "add":
        # Регулярное выражение для проверки команды. (УЖАС)
        pattern = r'^/add (.+)$'
        match = re.match(pattern, command)
        if match:
            return match.group(1)
        return False
    # Проверка команды /complete
    elif type_of_command == 'complete':
        pattern = r'^/complete ([1-9][0-9]*)$'
        match = re.match(pattern, command)
        if match:
            return match.group(1)
        return False
    # Проверка команды /del
    elif type_of_command == 'delete':
        pattern = r'^/del ([1-9][0-9]*)$'
        match = re.match(pattern, command)
        if match:
            return match.group(1)
        return False
    elif type_of_command == 'fdelete':
        if command.isdigit():
            return command
        else:
            return False
    else:
        return False

async def isvalidname(name, type_of_name):
    # Проверка название группы
    if type_of_name == 'group':
        if await check_group_name(name):
            return True
        return False
    if type_of_name == 'vgroup':
        name = str(name)
        vname = name.replace(' ', '')
        if vname.isalnum():
            return name
        else:
            return False
    else:
        return False