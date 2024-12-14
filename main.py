from asyncio import run
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram import types, F, Bot, Dispatcher
from message_commands import *
from bot_token import *
dp = Dispatcher()
print('Format of info about users is Full_name:tgID')

#Запуск бота командой /start
@dp.message(Command('start'))
async def start_bot(message: types.Message):
    full_name, user_id, username = message.from_user.full_name, message.from_user.id, message.from_user.username
    await add_user_to_data_base(user_id, full_name, username)
    print(f'{message.from_user.full_name}:{message.from_user.id} started this bot')

    kb = [
        [types.InlineKeyboardButton(text='Меню📖', callback_data='main_menu')], # Меню
        [
        types.InlineKeyboardButton(text='Информация👨‍💻', callback_data='information'), # Инфо
        types.InlineKeyboardButton(text='Список Админов👑', callback_data='list_of_admins') # Список Адм
        ]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    photo_data = 'AgACAgIAAxkBAANfZ1cpKZtmA3d5-GKxdt9eZfvaT5AAAqDnMRtq4sBKjGpk29o6-AwBAAMCAAN5AAM2BA'
    text_data = f"\n<b>Здравствуйте, {html.escape(message.from_user.full_name)}!</b>\nНиже кнопки которые вам понадобятся\n"
    await message.answer_photo(photo=photo_data, caption=text_data, reply_markup=keyboard)

#=====================================================================================# Начало кода основанного на F.Data

# Список админов, когда человек нажал на кнопку 'Список Админов👑'
@dp.callback_query( F.data == 'list_of_admins' )
async def admin_list(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_start")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = 'Список администраторов данного бота:\n1.@Marzkv👑'
    await callback.message.edit_caption(caption=text_data,reply_markup=keyboard)

# Информация о боте, когда человек нажал на кнопку 'Информация👨‍💻'
@dp.callback_query( F.data == 'information' )
async def information(callback: types.CallbackQuery):
    kb = [[types.InlineKeyboardButton(text="Вернуться назад", callback_data="back_to_start")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = '1. Запуск первой бета-версии: 13.12.2024'
    await callback.message.edit_caption(caption=text_data, reply_markup=keyboard)

# Возвращение пользователя в начальное меню
@dp.callback_query( F.data == 'back_to_start' )
async def start_bot_2(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton(text='Меню📖', callback_data='main_menu')], # Меню
        [types.InlineKeyboardButton(text='Информация👨‍💻', callback_data='information'),types.InlineKeyboardButton(text='Список Админов👑', callback_data='list_of_admins')], # Инфо , Список адм
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = f"\n<b>Здравствуйте, {html.escape(callback.from_user.full_name)}!</b>\nНиже кнопки которые вам понадобятся\n"
    await callback.message.edit_caption(caption=text_data,reply_markup=keyboard)

@dp.callback_query( F.data == 'commands_of_bot')
async def cmdlist(callback: types.CallbackQuery):
    kb = [[types.InlineKeyboardButton(text='Вернуться назад', callback_data='main_menu')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = f'1./add - Добавить задачу.\n2. /list - Список задач.\n3. /complete или /del - Удалить задачу.\n4. /clist - Список выполненных задач.'
    await callback.message.edit_caption(caption=text_data, reply_markup=keyboard)

@dp.callback_query( F.data == 'main_menu' )
async def main_menu(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton(text='Вернуться в начало', callback_data='back_to_start'), types.InlineKeyboardButton(text='Команды бота', callback_data='commands_of_bot')],
        [types.InlineKeyboardButton(text='Создать задачу', callback_data='create_task')],
        [types.InlineKeyboardButton(text='Список ваших задач', callback_data='list_of_tasks'), types.InlineKeyboardButton(text='Список завершенных задач', callback_data='completed_task_list')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    text_data = f'Вы находитесь в меню, ниже кнопки для удобной навигации'
    await callback.message.edit_caption(caption=text_data, reply_markup=keyboard)

#=====================================================================================# Конец кода основанного на F.Data



#=====================================================================================# Начала кода основанного на командах

# Команды в message_commands.py

# Добавление задачи в список задач
@dp.message( Command( 'add' ) )
async def add_task(message: types.Message):
    msg = html.escape(message.text)
    user_id = message.from_user.id
    text_data = await add_task_to_list(msg, user_id)
    await message.answer(text_data)

# Получение списка задач
@dp.message( Command ('list') )
async def get_list(message: types.Message):
    user_id = message.from_user.id
    tasks = await get_active_task_list(user_id)
    text_data = await get_task_list(tasks)
    await message.answer(text=text_data)

# Завершение задачи
@dp.message( Command( 'del' ) )
@dp.message( Command( 'complete' ) )
async def del_task(message: types.Message):
    msg = html.escape(message.text)
    user_id = message.from_user.id
    text_data = await delete_task_from_task_list(msg, user_id)
    await message.answer(text_data)

# Получение списка выполненных задач
@dp.message( Command ('Clist') )
@dp.message( Command ('clist') )
async def get_clist(message: types.Message):
    user_id = message.from_user.id
    text_data = await list_of_completed_tasks(user_id)
    await message.answer(text_data)

#=====================================================================================# Конец кода основанного на командах

# Если была введена неверная команда.
@dp.message(F.text[0] == '/')
async def wrong_command(message: types.Message):
    msg = message.text
    kb = [[types.InlineKeyboardButton(text='Команды бота', callback_data='commands_of_bot')]]
    text_data = f'Введенной вами команды "{msg}" - не существует\nНажав на кнопку ниже вы увидете доступные команды'
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    photo_data = 'AgACAgIAAxkBAANfZ1cpKZtmA3d5-GKxdt9eZfvaT5AAAqDnMRtq4sBKjGpk29o6-AwBAAMCAAN5AAM2BA'
    await message.answer_photo(photo=photo_data, caption=text_data, reply_markup=keyboard)

# Запуск бота
async def main():
    print('Введите пароль от бота')
    token_of_bot = await get_token(input())
    bot = Bot(token=token_of_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # API бота
    await dp.start_polling(bot)
if __name__ == "__main__":
    run( main() )