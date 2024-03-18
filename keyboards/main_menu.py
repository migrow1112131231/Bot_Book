from aiogram import Bot
from aiogram.types import BotCommand
from handbook import handbook, handbook_commands

async def set_main_menu(bot: Bot):
    commands = [BotCommand(
        command=key,
        description=value) for key, value in handbook_commands.items()]
    await bot.set_my_commands(commands)