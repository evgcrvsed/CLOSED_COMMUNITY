import json, random, asyncio
from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError

from dotenv import load_dotenv
load_dotenv()

from main import db, bot_main

texts = [
    """
__*ВЫ ТУТ\?*__

🤑 *ДЕНЬГИ* _*УЖЕ ГОТОВЫ К ПЕРЕВОДУ\!*_ 

✅ ВАМ ОДОБРЕН ЗАЙМ до 100\.000 RUB под 0%\! 💰
    """,
    """
👑 Следующие __*100*__ заявок будут одобрены в _*приоритетном порядке*_\!

🏦 Заявок уже одобрено \- 85

⬇️ Скорей нажимай на кнопку
    """,
    """
💰 _*Вам нужны деньги\?*_

✅ Ваши заявки одобрены уже как *2 часа*, а Вы до сих пор не забрали свои __*30 000 рублей\!*__ В чем дело\? 😲

💰 Нажмите на кнопку ниже ниже, заполните заявки по шагам, и Вы получите _деньги_
    """,
    """
⏳ _Уведомляем_ __*Вас*__, что *деньги находятся в режиме ожидания*

💰 Вам доступно для вывода до _*30\.000 ₽*_\!

⬇️ Получить можно здесь
    """,
    f"""
✅ Вы прошли *_процедуру одобрения_* от `{datetime.now().strftime("%d.%m.%Y")}`\!

💸 Вам доступно до _*30\.000*_ рублей\!

⬇️ Получить
    """,
    """
💳 _*Готовьте вашу карту*_\!

💸 *Перевод через 10 мин\!*

⬇️ Для получения заполните любую анкету:
    """,
    f"""
Решение по вашей заявке \#{random.randint(30000, 90000)}

✅ Одобрено на персональных условиях\. Действительно до `{datetime.now().strftime("%d.%m.%Y")}`

💸 Cредства готовы к переводу\! Забрать до 30\.000 рублей уже сегодня можно по кнопке снизу\!
    """,
    """
💸 _*Зачислено до 30\.000 RUB\!*_

่✅ _Рекомендуем подтвердить получение_ до 23:59\!

⬇️ Сегодня эти компании одобряют до 98,6% всех заявок\! Забери до 30\.000 рублей уже сегодня\!
    """
]


def send_notification_start():
    asyncio.gather(send_notification())


async def send_notification():
    with open('data/notifications_text.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Если список пуст, восстановить его до начального состояния
    if len(data['data']) == 0:
        data['data'] = texts.copy()

    # Выбор случайного текста и удаление его из списка
    text_to_send = random.choice(data['data'])
    data['data'].remove(text_to_send)

    # Сохранение обновленного списка в файл
    with open('data/notifications_text.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    button_text = ['Получить займ!', 'Забрать деньги!', 'Взять займ!', 'Получить!', 'Узнать подробнее..']
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f'💰 {random.choice(button_text)}', callback_data='profile_delete'))

    users_id = db.get_all_users()
    for user_id in users_id:
        try:
            await bot_main.send_message(chat_id=user_id, text=text_to_send, reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN_V2)
            await asyncio.sleep(5)
        except TelegramForbiddenError:
            db.delete_user(user_telegram_id=user_id)
        except Exception as ex:
            print(ex)