from config import Config, add_config
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import users_handlers
from keyboards import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    config: Config = add_config()
    dp = Dispatcher()
    bot = Bot(config.telegram_bot.token)

    dp.include_router(users_handlers.router)
    dp.startup.register(set_main_menu)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
