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


@router.callback_query(F.data == 'about_us')
async def about_us(clb) -> None:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data='start'))

    text = """
Закрытый канал CLOSED COMMUNITY — это моё дитя, моё творение, тот продукт, который поможет создать опору женственности и уверенности в себе любой женщина, тот набор знаний и то окружение, которые в комплексе будут способны заменить многим ребятам модель мамы\. Человека, которого у них никогда не было\. 

Полноценная школа женского воспитания, лучшая из школ, ведь только в ней есть ШКОЛА ЖИЗНИ\! 

Зачем мне это всё\?

Деньги \= заработок \+ возможность развиваться и расти\.

В первую очередь я рассматриваю запуск приватного канала, как наше ракетное топливо для выхода в стратосферу\. Я хочу создать ЛУЧШЕЕ и самое МАСШТАБНОЕ сообщество, а для этого нужны огромные деньги\. Несколько миллионов уже потрачено, но этого мало\. 90% от того, что будет приносить мне закрытый канал, я первые пол года\-год буду реинвестировать в рекламу, чтобы такое явление как «аленизм» было полностью уничтожено в нашем мире и мужчины вернули себе прежнюю силу и уверенность\.

ХОЧЕШЬ К НАМ\? ЖМИ ВНИЗУ НА КНОПКУ «ТАРИФЫ» И ЗАЛЕТАЙ, МЫ ТЕБЯ ЖДЕМ 🔥
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
