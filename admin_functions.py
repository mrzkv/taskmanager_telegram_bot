from data_base_functions import *

async def get_admin_statistics():
    count_users = await get_users_count()
    text_data = f'Статистика.\nВсего пользователей бота - {count_users}.'
    return text_data

admin_ids =[
    '5414402301'
]

async def isAdmin(user_id):
    if user_id in admin_ids:
        return True
    return False