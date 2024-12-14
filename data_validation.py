import re
# Валидация данных.
async def isvalid(command, type_of_command):
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
    else:
        return False
