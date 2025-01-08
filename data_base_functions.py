import asyncio
from aiogram.types import InlineKeyboardButton
from aiogram import types
import aiosqlite
import html

from flask.helpers import get_root_path


# Функция для получения списка завершенных задач из базы данных. Вызывается командой /clist
async def get_completed_task_list(user_id):
    completed_task_list = []
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(f"SELECT task FROM tasks WHERE user_id = {user_id} and is_deleted = 1 ORDER BY id ASC") as cursor:
            async for row in cursor:
                completed_task = row[0]
                completed_task_list.append(completed_task)
    return completed_task_list

# Функция для получения списка активных задач. Вызывается командой /list
async def get_active_task_list(user_id):
    task_list = []
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(f"SELECT task FROM tasks WHERE user_id = {user_id} and is_deleted = 0 ORDER BY id ASC") as cursor:
            async for row in cursor:
                task = row[0]
                task_list.append(task)
    return task_list

# Функция для получения ID в базе данных для активных задач. (Вспомогательная функция для завершения задач)
async def get_id_task_list(user_id):
    id_task_list = []
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(f"SELECT id FROM tasks WHERE user_id = {user_id} and is_deleted = 0 ORDER BY id ASC") as cursor:
            async for row in cursor:
                id_task = row[0]
                id_task_list.append(id_task)
    return id_task_list

# Добавление людей в базу данных Sqlite.
async def add_user_to_data_base(user_id, full_name, username):
    connect = await aiosqlite.connect('users.db') # Название базы данных
    cursor = await connect.cursor()
    check_user = await cursor.execute('SELECT * FROM users WHERE user_id = ?', # SQL запрос
                                     (user_id,))
    check_user = await check_user.fetchone()
    if check_user is None:
        await cursor.execute('INSERT INTO users (user_id, full_name, username) VALUES (?, ?, ?)',
                             (user_id, full_name, username))
        print(f"{full_name}:{user_id} added to data base.")
        await connect.commit()
    await cursor.close()
    await connect.close()


# Маркировка задачи как завершенная
async def delete_task(id_of_tasks):
    connect = await aiosqlite.connect('users.db') # Название базы данных
    cursor = await connect.cursor()
    await cursor.execute(f'UPDATE tasks SET is_deleted = 1 WHERE id = {id_of_tasks}')
    await connect.commit()
    await cursor.close()

# Подсчет кол-ва пользователей
async def get_users_count():
    connect = await aiosqlite.connect('users.db')
    cursor = await connect.cursor()
    user_count = await cursor.execute('SELECT COUNT(*) FROM users')
    user_count = await user_count.fetchone()
    await connect.commit()
    await cursor.close()
    return user_count[0]

# Добавление задач в базу данных Sqlite.
async def add_task_to_database(task, user_id):
    is_deleted = 0
    connect = await aiosqlite.connect('users.db') # Название базы данных
    cursor = await connect.cursor()
    await cursor.execute('INSERT INTO tasks (user_id, task, is_deleted) VALUES (?, ?, ?)', # SQL запрос
                         (user_id, task, is_deleted))
    await connect.commit()
    await cursor.close()

async def mark_task_in_db(msg, user_id):
    # Валидация данных №2(поиск в базе такой задачи)/ если успешно то задача маркируется 0 -> 1
    tasks = await get_active_task_list(user_id)
    if len(tasks) == 0:
        text_data = 'Ваш список задач пуст. Вы можете создать новую используя /add или кнопки'
        return text_data

    id_of_tasks = await get_id_task_list(user_id)
    if len(id_of_tasks) < int(msg) or int(msg) == 0:
        text_data = f'Введенный вами номер ("{msg}") не содержится в списке ваших задач'
        return text_data

    task_for_marked = id_of_tasks[int(msg)-1]
    await delete_task(task_for_marked)
    text_data = f'Задача "{tasks[int(msg)-1]}" под номером {msg} была завершена.\nЧтобы увидеть список завершенных задач /clist или использовать кнопки'
    return text_data

async def get_all_users_id():
    connect = await aiosqlite.connect('users.db')
    cursor = await connect.cursor()
    all_ids = await cursor.execute('SELECT user_id FROM users')
    all_ids = await all_ids.fetchall()
    await cursor.close()
    await connect.close()
    return all_ids

async def get_tasks_count():
    connect = await aiosqlite.connect('users.db')
    cursor = await connect.cursor()
    all_tsks = await cursor.execute('SELECT COUNT(*) FROM tasks')
    all_tsks = await all_tsks.fetchone()
    await cursor.close()
    await connect.close()
    return all_tsks[0]

async def check_group_name(name):

    connect = await aiosqlite.connect('users.db')
    cursor = await connect.cursor()
    current_group_name = await cursor.execute('SELECT * FROM groups WHERE name = ?', (name,))
    current_group_name = await current_group_name.fetchone()
    await cursor.close()
    await connect.close()
    if current_group_name is None:
        return True
    else:
        return False



async def create_group_db(name, creator):
    connect = await aiosqlite.connect('users.db')
    cursor = await connect.cursor()
    await cursor.execute('INSERT INTO groups (name, creator) VALUES (?, ?)',
                         (name, creator))
    await cursor.close()
    await connect.commit()
    await connect.close()

async def get_kb_for_user_group(id):
    connect = await aiosqlite.connect('users.db')
    cursor = await connect.cursor()
    group_list = await cursor.execute('SELECT name FROM group_participants WHERE participant = ? ORDER BY id ASC', (id,))
    group_list = await group_list.fetchall()
    await cursor.close()
    await connect.close()
    if not group_list:
        return False
    else:
        kb = []
        len_grplist = len(group_list)
        len_grplist2 = len_grplist
        for i in range(0,len_grplist2,3):
            if len_grplist >= 3:
                len_grplist -= 3
                kb.append(
                    [types.InlineKeyboardButton(text=html.escape(group_list[i][0]), callback_data=html.escape(f'usergroup-{group_list[i][0]}')),
                     types.InlineKeyboardButton(text=html.escape(group_list[i+1][0]), callback_data=html.escape(f'usergroup-{group_list[i+1][0]}')),
                     types.InlineKeyboardButton(text=html.escape(group_list[i+2][0]), callback_data=html.escape(f'usergroup-{group_list[i+2][0]}'))])
                continue
            elif len_grplist == 2:
                len_grplist -= 2
                kb.append(
                    [types.InlineKeyboardButton(text=html.escape(group_list[i][0]),callback_data=html.escape(f'usergroup-{group_list[i][0]}')),
                     types.InlineKeyboardButton(text=html.escape(group_list[i+1][0]), callback_data=html.escape(f'usergroup-{group_list[i+1][0]}'))])
                continue
            else:
                len_grplist -= 1
                kb.append(
                    [types.InlineKeyboardButton(text=html.escape(group_list[i][0]),callback_data=html.escape(f'usergroup-{group_list[i][0]}'))])
                continue
        return kb


async def get_kb_for_creator_groups(id):
    connect = await aiosqlite.connect('users.db')
    cursor = await connect.cursor()
    group_list = await cursor.execute('SELECT name FROM groups WHERE creator = ? ORDER BY id ASC', (id,))
    group_list = await group_list.fetchall()
    await cursor.close()
    await connect.close()
    if group_list == []:
        return False
    else:
        kb = []
        len_grplist = len(group_list)
        len_grplist2 = len_grplist
        for i in range(0,len_grplist2,3):
            if len_grplist >= 3:
                len_grplist -= 3
                kb.append(
                    [types.InlineKeyboardButton(text=html.escape(group_list[i][0]), callback_data=html.escape(f'ownergroup-{group_list[i][0]}')),
                     types.InlineKeyboardButton(text=html.escape(group_list[i+1][0]), callback_data=html.escape(f'ownergroup-{group_list[i+1][0]}')),
                     types.InlineKeyboardButton(text=html.escape(group_list[i+2][0]), callback_data=html.escape(f'ownergroup-{group_list[i+2][0]}'))])
                continue
            elif len_grplist == 2:
                len_grplist -= 2
                kb.append(
                    [types.InlineKeyboardButton(text=html.escape(group_list[i][0]),callback_data=html.escape(f'ownergroup-{group_list[i][0]}')),
                     types.InlineKeyboardButton(text=html.escape(group_list[i+1][0]), callback_data=html.escape(f'ownergroup-{group_list[i+1][0]}'))])
                continue
            else:
                len_grplist -= 1
                kb.append(
                    [types.InlineKeyboardButton(text=html.escape(group_list[i][0]),callback_data=html.escape(f'ownergroup-{group_list[i][0]}'))])
                continue
        return kb