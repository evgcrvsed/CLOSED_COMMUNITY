from pprint import pprint
from aiogram import Router

from main import db, bot_main

router = Router()


async def send_user_message(user_id, text):
    try:
        await bot_main.send_message(chat_id=user_id, text=text)
    except Exception as ex:
        print('Не удалось отправить сообщение:')
        print(ex)


@router.chat_join_request()
async def chat_join_handler(clb):
    pprint(clb)

    db.add_user(user_telegram_id=clb.from_user.id)
    db.set_group_joined_true(user_telegram_id=clb.from_user.id)

    await clb.approve()
