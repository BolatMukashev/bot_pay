from aiogram.types import CallbackQuery
from bot import dp, bot
from keyboards.inline.callback_datas import set_country
from keyboards.inline.start_button import start_keyboard
from db_operations import edit_user_country, get_user_language
from messages import MESSAGE, IMAGES, TEST_IMAGES
from db_operations import get_user_registration_status, get_user_by, get_time_limit
import config


@dp.callback_query_handler(set_country.filter(country='country'))
async def update_country(call: CallbackQuery, callback_data: dict):
    telegram_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_country = callback_data.get('value')
    edit_user_country(telegram_id, user_country)
    user_language = get_user_language(telegram_id)

    await call.answer(MESSAGE[f'country_edited_ok_{user_language}'], cache_time=1)
    await call.message.edit_reply_markup()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=MESSAGE[f'country_edited_ok_{user_language}'])
    if not get_user_registration_status(telegram_id):
        user = get_user_by(telegram_id)
        daily_limit = config.TARIFFS[user.tariff]['daily_limit'] + (5 * user.referral_bonus)
        _, limit_time = get_time_limit(user)
        text = MESSAGE[f'registration_ok_{user_language}'].format(config.TARIFFS[user.tariff]['translate'], daily_limit,
                                                                  limit_time)
        image = TEST_IMAGES[f'tariffs_{user_country}_{user_language}'] if config.DEBUG else IMAGES[
            f'tariffs_{user_country}_{user_language}']
        await bot.send_photo(telegram_id, image, caption=text, reply_markup=start_keyboard)
