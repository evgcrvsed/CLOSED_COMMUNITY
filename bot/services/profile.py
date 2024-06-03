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


class MyCallbackData(CallbackData, prefix="_"):
    param: str


@router.callback_query(F.data == 'profile_delete')
async def profile_delete(clb) -> None:
    buttons_data = db.get_buttons_data()
    # pprint(buttons_data)

    buttons_locked: list = []
    if type(clb) is CallbackQuery:
        buttons_locked = db.get_buttons_locked(user_telegram_id=clb.message.chat.id)
    elif type(clb) is Message:
        buttons_locked = db.get_buttons_locked(user_telegram_id=clb.chat.id)

    # pprint(buttons_locked)

    builder = InlineKeyboardBuilder()
    for index, button in enumerate(buttons_data):
        if index % 2 == 0:
            builder_state = True
        else:
            builder_state = False

        if button in buttons_locked:
            button_text = f'✅ {button}'
        else:
            button_text = f'{button}'

        callback_data = MyCallbackData(param=button).pack()
        if builder_state:
            builder.row(InlineKeyboardButton(text=button_text, callback_data=callback_data))
        else:
            builder.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    builder.row(InlineKeyboardButton(text='💵 Забрать деньги!', callback_data='build_buttons_map'))

    text = """
__*ℹ️ Важная информация*__

💎 Чтобы мы смогли подобрать для вас самое *выгодное* и *беспроцентное* ~%%%~ _*предложение*_ 

⬇️ Из представленных организаций ниже, выберете те, в которых вы ещё __*не брали займ*__:    
    """

    if type(clb) is CallbackQuery:
        message = clb.bot.edit_message_reply_markup
        await message(
            chat_id=clb.message.chat.id,
            message_id=clb.message.message_id,
            reply_markup=builder.as_markup()
        )

        await clb.message.edit_text(
            text=text,
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


@router.callback_query(MyCallbackData.filter())
async def handle_callback(clb: types.CallbackQuery, callback_data: MyCallbackData):
    param = callback_data.param
    # print(clb.message.chat.id)
    db.switch_buttons_locked(user_telegram_id=clb.message.chat.id, name=param)
    # await clb.message.answer(f"Button clicked with parameter: {param}")
    print(f'name:@{clb.from_user.first_name} id:{clb.message.chat.id} pressed:{param}')
    try:
        await profile_delete(clb)
    except Exception as ex:
        pass


@router.callback_query(F.data == 'button_name')
async def button_name(clb) -> None:
    print(f'Нажата кнопка с названием {button_name}')
    await db.switch_buttons_locked(user_telegram_id=clb.chat.id, name=button_name)


@router.callback_query(F.data == 'build_buttons_map')
async def build_buttons_map(clb: types.CallbackQuery) -> None:
    buttons_data = db.get_buttons_data()
    # pprint(buttons_data)
    buttons_locked: list = []
    if type(clb) is CallbackQuery:
        buttons_locked = db.get_buttons_locked(user_telegram_id=clb.message.chat.id)
    elif type(clb) is Message:
        buttons_locked = db.get_buttons_locked(user_telegram_id=clb.chat.id)

    builder = InlineKeyboardBuilder()
    builder_state: bool = True

    for button in buttons_data:
        # print(buttons_data[button])

        if button in buttons_locked:
            button_text = f'🌐 {button}'
            if builder_state:
                builder.row(InlineKeyboardButton(text=button_text, web_app=WebAppInfo(url=buttons_data[button])))
                builder_state = False
            else:
                builder.add(InlineKeyboardButton(text=button_text, web_app=WebAppInfo(url=buttons_data[button])))
                builder_state = True

    builder.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data='profile_delete'))

    text = """
🤑 *Отличная новость\!*

Чтобы получить займ от 2 до 100 тыс\. руб\. необходимо нажать на кнопку организации и заполнить анкету на сайте\. \(В течение 5 минут деньги придут вам на карту\):

🙋‍♀️Совет: чтобы увеличить вероятность и скорость одобрения займа, оставьте анкеты сразу в нескольких компаниях, а лучше во всех\!

💳 Займы только для Граждан Российской Федерации 🇷🇺\!
    """

    if type(clb) is CallbackQuery:

        message = clb.bot.edit_message_reply_markup
        await message(
            chat_id=clb.message.chat.id,
            message_id=clb.message.message_id,
            reply_markup=builder.as_markup()
        )

        await clb.message.edit_text(
            text=text,
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
