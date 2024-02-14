from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from core.handlers.basic import get_start, get_help, get_other, get_chat_id, get_you

from core.handlers.admin import set_mt, set_voting, output_to_group
# from core.handlers.contact import get_true_contact, get_fake_contact
# from core.handlers.callback import do_test

from core.handlers.valentine import *

from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as rediss

# from core.filters.iscontact import IsTrueContact
import asyncio
import asyncpg
import logging
from datetime import datetime, timedelta

from core.settings import settings
from core.utils.commands import set_commands
from core.utils.callbackdata import CallbackAddAsAuthor
from core.utils.statesform import Valentine

from core.middlewares.countermiddleware import CounterMiddleware
from core.middlewares.maintenance_middleware import MaintenanceMiddleware
from core.middlewares.voting_middleware import VotingMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.antiflood_middleware import ThrottlingMiddleware
from core.middlewares.appschmiddleware import SchedulerMiddleware

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator
from core.handlers import appsched


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Bot started.')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stopped.')


async def create_pool():
    return await asyncpg.create_pool(user='avnadmin', password='AVNS_IIjRhyiq2_zowhqUvOB', database='fknk',
                                             host='tmrwld-itsquwi-db6a.aivencloud.com', port=25553)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    pool_connect = await create_pool()
    storage = RedisStorage.from_url(
        f'redis://{settings.bots.redis_url}'
    )
    dp = Dispatcher(storage=storage)

    # jobstores = {
    #     'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
    #                              run_times_key='dispatched_trips_running',
    #                              host='redis-18647.c55.eu-central-1-1.ec2.cloud.redislabs.com',
    #                              port=18647,
    #                              password='fYoBaORVcVypmRMSLWQpLgN4Qsady3c6',
    #                              db=0)
    # }
    # scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Europe/Moscow", jobstores=jobstores,
                                                        #    job_defaults={'misfire_grace_time': 15*60}))
    # scheduler.ctx.add_instance(bot, declared_class=Bot)
    # scheduler.add_job(appsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10))
    # scheduler.add_job(appsched.send_message_cron, trigger='cron', hour=datetime.now().hour,
    #                   minute=datetime.now().minute + 1, start_date=datetime.now())
    # scheduler.add_job(appsched.send_message_interval, trigger='interval', seconds=30)

    # scheduler.start()

    redis_client = rediss.from_url(
        f'redis://{settings.bots.redis_url}'
    )

    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.middleware.register(CounterMiddleware())
    dp.message.middleware.register(MaintenanceMiddleware())
    dp.message.middleware.register(VotingMiddleware())
    dp.message.middleware.register(ThrottlingMiddleware(redis=redis_client))
    # dp.update.middleware.register(SchedulerMiddleware(scheduler))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # dp.callback_query.register(do_test, CallbackTestInfo.filter())  # F.(class property) == x | e.g. F.btn_num == 2
    # dp.message.register(get_true_contact, F.contact, IsTrueContact())
    # dp.message.register(get_fake_contact, F.contact)

    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(get_help, Command(commands='help'))

    dp.message.register(get_you, F.text.lower() == 'тебе')  # хочу тебе
    # dp.message.register(start_voting, Command(commands='vote'))

    # dp.callback_query.register(make_vote, CallbackStartVoting.filter(), UserVoting.START_VOTING)
    # dp.callback_query.register(ask_confirm_vote, CallbackVoting.filter(), UserVoting.CHOOSE_CANDIDATE)
    # dp.callback_query.register(confirm_vote, CallbackConfirmVoting.filter(F.todo == 'confirmed'), UserVoting.CONFIRM)
    # dp.callback_query.register(back_to_manu_vote, CallbackConfirmVoting.filter(F.todo == 'back'), UserVoting.CONFIRM)
    #
    # dp.callback_query.register(show_warning, CallbackStartVoting.filter())
    # dp.callback_query.register(show_warning, CallbackVoting.filter())
    # dp.callback_query.register(show_warning, CallbackConfirmVoting.filter(F.todo == 'confirmed'))
    # dp.callback_query.register(show_warning, CallbackConfirmVoting.filter(F.todo == 'back'))

    dp.message.register(valentine_start, Command(commands='love'))
    dp.message.register(valentine_get_cancel, Command(commands='lonely'))
    dp.message.register(valentine_get_to, Valentine.GET_TO)
    dp.message.register(valentine_get_message, Valentine.GET_MSG)
    dp.callback_query.register(valentine_get_from, CallbackAddAsAuthor.filter(), Valentine.GET_FROM)
    dp.callback_query.register(valentine_call_cancel, CallbackAddAsAuthor.filter())

    # Maintenance
    dp.message.register(set_mt, F.text == "mt", F.from_user.id == settings.bots.admin_id)
    dp.message.register(set_voting, F.text == "!v", F.from_user.id == settings.bots.admin_id)
    dp.message.register(output_to_group, Command(commands='say'), F.from_user.id == settings.bots.admin_id)
    dp.message.register(get_chat_id, Command(commands='chatid'), F.from_user.id == settings.bots.admin_id)

    # Everything else
    dp.message.register(get_other, F.text)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())
