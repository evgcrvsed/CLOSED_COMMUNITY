from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types.web_app_info import WebAppInfo
from aiogram.enums import ParseMode
from dotenv import load_dotenv
load_dotenv()

from main import db

router = Router()


@router.callback_query(F.data == 'my_subscribe_info')
async def my_subscribe_info(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='🌸 Купить подписку', callback_data='tariffs_main'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='start'))

    text = """
⌛️ У Вас нет действующей подписки\.
⬇️ Ознакомьтесь с тарифами, нажав на кнопку ниже\.
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
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif type(clb) is Message:
        previous_message = clb

        clb: Message = clb

        await clb.answer(
            text=text,
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.MARKDOWN_V2
        )

        await previous_message.delete()
