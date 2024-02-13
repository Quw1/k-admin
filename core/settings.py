from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    maintenance: int
    voting: int
    supergroup_id: str
    val_logs_id: str
    val_main_id: str
    redis_url: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            maintenance=0,
            voting=0,
            supergroup_id=env.str("SUPERGROUP_ID"),
            val_logs_id=env.int("VAL_LOGS_ID"),
            val_main_id=env.int("VAL_MAIN_ID"),
            redis_url=env.str("REDIS_URL"),
        )
    )


settings = get_settings('input')



