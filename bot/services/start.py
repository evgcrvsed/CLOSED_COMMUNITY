import os, time
from aiogram import Router, F, Bot, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.types.input_file import FSInputFile

from main import db, bot_main
from dotenv import load_dotenv
load_dotenv()

router = Router()


@router.callback_query(F.data == 'start')
@router.message(Command("start"))
async def start(clb) -> None:
    if type(clb) is Message:
        if str(clb.chat.id)[0] == '-':
            print('С группы сообщение')
            return

    if type(clb) is CallbackQuery:
        db.add_user(user_telegram_id=clb.message.chat.id)
    elif type(clb) is Message:
        db.add_user(user_telegram_id=clb.chat.id)

    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💵 Тарифы', callback_data='tariffs_main'))
    builder.row(InlineKeyboardButton(text='⏳ Моя подписка', callback_data='my_subscribe_info'))
    builder.row(InlineKeyboardButton(text='🔎 Подробнее о закрытом канале', callback_data='about_us'))

    text = """
Приветик, моя дорогая, этот бот поможет тебе попасть в моё приватное комьюнити  “CLOSED COMMUNITY”

Что тебя ждет в закрытом комьюнити?
✦ [Подробнее](https://t.me/evgcursed)

_Читаешь_ \- _*повторяешь*_ \- __*получаешь результат*__ 

Для того чтобы попасть в моё комьюнити и раз и на всегда забыть о проблемах с противоположным полом и выбери нужный тариф:
"""

    if type(clb) is CallbackQuery:
        message = clb.bot.edit_message_reply_markup
        await message(
            chat_id=clb.message.chat.id,
            message_id=clb.message.message_id,
            reply_markup=builder.as_markup()
        )

        await clb.message.edit_caption(
            caption=text,
            photo=FSInputFile('data/images/image_start.jpg'),
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif type(clb) is Message:
        previous_message = clb
        clb: Message = clb

        await clb.answer_photo(
            caption=text,
            photo=FSInputFile('data/images/image_start.jpg'),
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.MARKDOWN_V2
        )

        await previous_message.delete()


@router.callback_query(F.data == 'check_subscribe')
async def check_subscribe(clb) -> None:
    if not db.get_user_group_joined(user_telegram_id=clb.message.chat.id):
        await bot_main.answer_callback_query(callback_query_id=clb.id, text='Вы не подписались', show_alert=True)
        return

    # await profile_delete(clb)
