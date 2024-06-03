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


@router.callback_query(F.data == 'tariffs_main')
async def tariffs_main(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='🏵 1 месяц', callback_data='tariffs_1_1'))
    builder.row(InlineKeyboardButton(text='🌹 3 месяца (ВЫГОДНЕЕ ВСЕГО)', callback_data='build_buttons_map'))
    builder.row(InlineKeyboardButton(text='🌸 6 месяцев', callback_data='build_buttons_map'))
    builder.row(InlineKeyboardButton(text='🌺 12 месяцев', callback_data='build_buttons_map'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='start'))

    text = """
Оплачивая любой тариф на подписку, вы подтверждаете согласие с [офертой](https://telegra.ph/Oferta-11-24) и автосписанием средств, согласно вашему тарифному плану\.  
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


tariffs_text = """
Тариф: DATE
Стоимость: PRICE ₽
Срок действия: TIME

Вы получите доступ к следующим ресурсам:
"""


@router.callback_query(F.data == 'tariffs_1_1')
async def tariffs_1(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💵 Оплатить', callback_data='tariffs_1_2'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_main'))

    text = tariffs_text
    text = text.replace('DATE', '1 месяц 🏵')
    text = text.replace('PRICE ', '990')
    text = text.replace('TIME', '30 дней')

    text = f'{text}✦ Закрытый канал'
    text = f'{text}\n✦ Чат комьюнити'

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


@router.callback_query(F.data == 'tariffs_1_2')
async def tariffs_1_2(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💳 Банковская карта (любой страны)', callback_data='pay'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_1_1'))

    text = tariffs_text
    text = text.replace('DATE', '1 месяц 🏵')
    text = text.replace('PRICE ', '990')
    text = text.replace('TIME', '30 дней')

    text = text.replace('Вы получите доступ к следующим ресурсам:', 'Выберите способ оплаты:')

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


@router.callback_query(F.data == 'pay')
async def pay(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💳 Перейти к оплате', web_app=WebAppInfo(url='https://www.youtube.com')))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_1_2'))

    text = """
✅ Счёт на оплату сформирован\. Доступы к закрытым сообществам будут открыты, как только вы оплатите его\.
    """

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
