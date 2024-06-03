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
    builder.row(InlineKeyboardButton(text='🌹 3 месяца (ПОПУЛЯРНО)', callback_data='tariffs_3_1'))
    builder.row(InlineKeyboardButton(text='🌸 6 месяцев', callback_data='tariffs_6_1'))
    builder.row(InlineKeyboardButton(text='🌺 12 месяцев', callback_data='tariffs_12_1'))
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

    builder.row(InlineKeyboardButton(text='💳 Банковская карта (любой страны)', callback_data='pay_1'))
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


@router.callback_query(F.data == 'pay_1')
async def pay_1(clb) -> None:
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


# 3 МЕСЯЦА
@router.callback_query(F.data == 'tariffs_3_1')
async def tariffs_3(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💵 Оплатить', callback_data='tariffs_3_2'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_main'))

    text = tariffs_text
    text = text.replace('DATE', '3 месяца 🌹')
    text = text.replace('PRICE ', '~2970~ 2490')
    text = text.replace('TIME', '90 дней')

    text = f'{text}✦ Закрытый канал'
    text = f'{text}\n✦ Чат комьюнити'
    text = f'{text}\n✦ Гайды и чек листы'

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


@router.callback_query(F.data == 'tariffs_3_2')
async def tariffs_3_2(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💳 Банковская карта (любой страны)', callback_data='pay'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_3_1'))

    text = tariffs_text
    text = text.replace('DATE', '3 месяц 🌹')
    text = text.replace('PRICE ', '~2970~ 2490')
    text = text.replace('TIME', '90 дней')

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


@router.callback_query(F.data == 'pay_3')
async def pay_3(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💳 Перейти к оплате', web_app=WebAppInfo(url='https://www.youtube.com')))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_3_2'))

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


# 6 МЕСЯЦА
@router.callback_query(F.data == 'tariffs_6_1')
async def tariffs_6(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💵 Оплатить', callback_data='tariffs_6_2'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_main'))

    text = tariffs_text
    text = text.replace('DATE', '6 месяцев 🌸')
    text = text.replace('PRICE ', '~5490~ 4990')
    text = text.replace('TIME', '180 дней')

    text = f'{text}✦ Закрытый канал'
    text = f'{text}\n✦ Чат комьюнити'
    text = f'{text}\n✦ Гайды и чек листы'

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


@router.callback_query(F.data == 'tariffs_6_2')
async def tariffs_6_2(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💳 Банковская карта (любой страны)', callback_data='pay_6'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_6_1'))

    text = tariffs_text
    text = text.replace('DATE', '6 месяцев 🌸')
    text = text.replace('PRICE ', '~5490~ 4990')
    text = text.replace('TIME', '180 дней')

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


@router.callback_query(F.data == 'pay_6')
async def pay_6(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💳 Перейти к оплате', web_app=WebAppInfo(url='https://www.youtube.com')))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_6_2'))

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


# 12 МЕСЯЦА
@router.callback_query(F.data == 'tariffs_12_1')
async def tariffs_12(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💵 Оплатить', callback_data='tariffs_12_2'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_main'))

    text = tariffs_text
    text = text.replace('DATE', '12 месяцев 🌺')
    text = text.replace('PRICE ', '~11 880~ 10 990')
    text = text.replace('TIME', '365 дней')

    text = f'{text}✦ Закрытый канал'
    text = f'{text}\n✦ Чат комьюнити'
    text = f'{text}\n✦ Гайды и чек листы'

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


@router.callback_query(F.data == 'tariffs_12_2')
async def tariffs_12_2(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💳 Банковская карта (любой страны)', callback_data='pay_12'))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_12_1'))

    text = tariffs_text
    text = text.replace('DATE', '12 месяцев 🌺')
    text = text.replace('PRICE ', '~11 880~ 10 990')
    text = text.replace('TIME', '365 дней')

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


@router.callback_query(F.data == 'pay_12')
async def pay_12(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='💳 Перейти к оплате', web_app=WebAppInfo(url='https://www.youtube.com')))
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='tariffs_12_2'))

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