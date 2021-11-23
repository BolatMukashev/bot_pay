from aiogram.types import CallbackQuery

import config
from bot import dp, bot, send_pay_access_message
from keyboards.inline.button_with_url import get_url_button
from keyboards.inline.callback_datas import pay_button_call
from db_operations import PayData
import messages
from db_operations import get_user_by
from pay_system_ioka import PayLinkIoka


@dp.callback_query_handler(pay_button_call.filter(pay_button='pay_button'))
async def get_pay_link_button(callback: CallbackQuery, callback_data: dict):
    """
    Команда pay посылает запрос в платежную систему, получает в ответ платежную ссылку и передает эту ссылку на оплату
    клиенту
    """
    telegram_id = callback.from_user.id
    purchased_tariff = callback_data.get('value')
    user = get_user_by(telegram_id)
    pay_data = PayData(user, purchased_tariff)
    pay_link = PayLinkIoka(telegram_id=telegram_id, price=pay_data.price_tenge, currency=pay_data.code,
                           name=user.full_name, tariff=purchased_tariff)
    await callback.answer()

    image = messages.IMAGES[f'tariff_{purchased_tariff}_{user.language}'] if not config.DEBUG else messages.TEST_IMAGES[
        f'tariff_{purchased_tariff}_{user.language}']
    link_button = get_url_button(messages.BUTTONS[f'pay_{user.language}'], pay_link.get_pay_url())
    await bot.send_photo(telegram_id, image)
    await bot.send_message(telegram_id, pay_data.message_text, reply_markup=link_button)
    await send_pay_access_message(telegram_id, user.language, 20)
