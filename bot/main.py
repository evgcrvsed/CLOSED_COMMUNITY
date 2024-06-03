import os, asyncio, logging, schedule

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from data.DataBase import DataBase

from dotenv import load_dotenv
load_dotenv()

db = DataBase('data/database.db')

bot_main = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

from services import start, chat_join_request_handler, profile, notifications


async def main_bot():
    dp = Dispatcher()

    dp.include_routers(
        profile.router,
        start.router,
        chat_join_request_handler.router
    )

    await bot_main.delete_my_commands()

    basic_commands = [
        BotCommand(command="/start", description="Начать")
    ]
    await bot_main.set_my_commands(commands=basic_commands)

    await dp.start_polling(bot_main, skip_updates=True)


async def waiter():
    while True:
        await asyncio.sleep(30)
        schedule.run_pending()


async def main():
    schedule.every().day.at("10:00").do(notifications.send_notification_start)
    schedule.every().day.at("14:00").do(notifications.send_notification_start)
    schedule.every().day.at("18:00").do(notifications.send_notification_start)

    # await notifications.send_notification()
    await asyncio.gather(main_bot(), waiter())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    db.create_table()
    asyncio.run(main())