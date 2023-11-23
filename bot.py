import time
import asyncio
import logging
import json
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, URLInputFile)
from aiogram.enums import ParseMode
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config, load_config
from db.db_tools import check_user, check_admin, check_not_free, check_payment

logger = logging.getLogger(__name__)

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command(commands=['quest']))
async def check(message):
    qid = 2
    free = await check_not_free(qid)
    print(free)
    if free is True:
        if await check_payment(message.from_user.id, qid):
            await message.answer('Доступ к квесту разрешен')
        else:
            await message.answer('Требуется оплата')
    else:
        await message.answer('Квест бесплатен!')




@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    """заглушка на сообщения"""

    print(message.from_user)
    a = await check_user(message.from_user)
    await check_admin(message.from_user.id)
    logging.info(f'Пользователь есть: {a[0]}, {message.from_user.id}, {message.from_user.username}')
    if a[0] is True:
        await message.reply(text='Привет!')
    else:
        await  message.reply(text='Велкоме!')
    await message.reply(text='Извините, моя твоя не понимать')


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot_data')

    # Загружаем конфиг в переменную config
    # config: Config = load_config()

    # # Инициализируем бот и диспетчер
    # bot: Bot = Bot(token=config.tg_bot.token,
    #                parse_mode='HTML')
    # dp: Dispatcher = Dispatcher(storage=MemoryStorage())

    # Настраиваем главное меню бота
    #await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    # dp.include_router(user_handlers.router)
    # dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())