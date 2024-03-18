from environs import Env
from dataclasses import dataclass as dt

@dt
class TelegramBot:
    token: str
    admins: 'int | list[int]'

@dt
class Config:
    telegram_bot: TelegramBot

def add_config():
    env = Env()
    env.read_env()

    return Config(
        telegram_bot=TelegramBot(
            token=env('BOT_TOKEN'),
            admins=list(map(int, env.list('ADMINS')))
        )
    )