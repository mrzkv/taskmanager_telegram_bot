import html
from data_base_functions import *
from data_validation import *
async def delete_task_from_task_list(msg, user_id):
    # Валидация данных(корректность ввода команды)
    if msg[0:4] == '/del':
        valid_msg = await isvalid(f'{msg}', 'delete')
    elif msg[0:9] == "/complete":
        valid_msg = await isvalid(f'{msg}', 'complete')
    if not valid_msg:
        text_data = f'Скорее всего вы неправильно ввели команду.\nФормат ввода команды: /del или /complete {html.escape("<номер задачи>")}\nВы ввели: {html.escape(msg)}'
        return text_data
    # Валидация данных №2(поиск в базе такой задачи)/ если успешно то задача маркируется 0 -> 1
    text_data = await mark_task_in_db(valid_msg, user_id)
    return text_data

async def add_task_to_list(msg, user_id):
    task_name = (await isvalid(f'{msg}', 'add'))
    if not task_name:
        text_data = f'Скорее всего вы неправильно ввели команду.\nФормат ввода команды: /add {html.escape("<название задачи>")} \nпричем использовать можно только русские или английские буквы и спец.символы вида - ! @ # % )\nВы ввели: {html.escape(msg)}'
        return text_data
    else:
        await add_task_to_database(f'{task_name}', f'{user_id}')
        text_data = f'Задача: <pre language="Task">{html.escape(task_name)}</pre> добавлена в список задач'
        return text_data

async def get_task_list(tasks):
    if len(tasks) != 0:
        string_tasks = '<b>'
        for i in range(len(tasks)):
            string_tasks += f'{i+1}. {tasks[i]}'
            string_tasks += '\n'
        string_tasks += '</b>'
        text_data = f'Список ваших задач:\n{string_tasks}'
    else:
        text_data = 'Ваш список задач пуст. Вы можете создать новую используя /add'

    return text_data


async def list_of_completed_tasks(user_id):
    list_of_completed = await get_completed_task_list(user_id)
    if len(list_of_completed) == 0:
        text_data = f"Ваш список завершенных задач пуст.\nЧтобы завершить задачу можете воспользоваться:\n/del <b>{html.escape('<Номер задачи>')}</b> или /compelte <b>{html.escape('<Номер задачи>')}</b>"
    else:
        string_tasks = '<b>'
        for i in range(len(list_of_completed)):
            string_tasks += f'{i + 1}. {list_of_completed[i]}'
            string_tasks += '\n'
        string_tasks += '</b>'
        text_data = f'Список ваших завершенных задач:\n{string_tasks}'
    return text_data

