from aiogram import Bot
from aiogram.types import Message
from core.utils.dbconnect import Request
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.enums.chat_member_status import ChatMemberStatus
from core.utils.callbackdata import CallbackAddAsAuthor
from core.keyboards.inline import get_yes_no_markup
from core.utils.statesform import Valentine
from core.settings import settings
from aiogram.types.link_preview_options import LinkPreviewOptions
import html
from core import settings


async def valentine_start(message: Message, bot: Bot, request: Request, state: FSMContext):
    if message.chat.type != 'private':
        await message.reply('приймаю лише в приватних повідомленнях <3')
    else:
        await message.answer('ну давай, кого любимо на цей раз?\n\nнапиши у форматі <b>@username</b>\n\nякщо у людини нема '
                             '@username, можеш написати її ім\'я так, щоб вона змогла знайти валентинку (наприклад: '
                             'Діма Остапенко К-24\n\n<i>якщо захочеш зупинити процес, тикай /lonely (тю, навіть не спробуєш?)</i>')
        await state.set_state(Valentine.GET_TO)


async def valentine_get_to(message: Message, bot: Bot, request: Request, state: FSMContext):
    if not message.text:
        await message.answer('чел ти... напиши текстом нік/ім\'я')
    else:
        if len(message.text) > 30:
            pass
        elif len(message.text) < 6:
            await message.answer('пиши нормально - мінімум 5 букв')
        else:
            to = message.text.replace("_", "\\_")\
                .replace("*", "\\*")\
                .replace("[", "\\[")\
                .replace("`", "\\`")
            to = html.escape(to)

            if to.isascii() and ' ' not in to and '@' not in to:
                to = '@' + to

            await state.update_data(to=to)
            await state.set_state(Valentine.GET_MSG)
            await message.answer('а тепер шо ти хочеш людині сказати?\n\nнадсилай або текстове повідомлення, або кидай '
                                 'фотку/картинку\n\nнаприклад, звідси: \nрекомендую на картинці вказати кому та від '
                                 'кого ще раз :)\n\nP.S: якщо хочеш хочоеш шось інше за текст або фотку, то напиши '
                                 'адмінам @')


async def valentine_get_message(message: Message, bot: Bot, request: Request, state: FSMContext):
    if (not message.text) and (not message.photo):
        await message.answer('дозволені лише фотки та текстові повідомлення\n\nале якшо дуже хочеш щось інше, можеш '
                             'домовитись з адмінами 🤑 @')
    else:
        if message.text:
            msg = message.text.replace("_", "\\_") \
                .replace("*", "\\*") \
                .replace("[", "\\[") \
                .replace("`", "\\`")
            msg = html.escape(msg)
            await state.update_data(text=msg)
        else:
            if message.caption is not None:
                msg = message.caption.replace("_", "\\_") \
                    .replace("*", "\\*") \
                    .replace("[", "\\[") \
                    .replace("`", "\\`")
                msg = html.escape(msg)
                await state.update_data(text=msg)

            await state.update_data(photo=message.photo[-1].file_id)
        await message.answer('супер!\n\nдодати тебе як автора?', reply_markup=get_yes_no_markup())
        await state.set_state(Valentine.GET_FROM)


async def valentine_get_from(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackAddAsAuthor,
                             state: FSMContext):
    data = await state.get_data()
    add_author = callback_data.todo
    to = data.get('to')
    text = data.get('text')
    photo = data.get('photo')
    user = call.from_user
    if callback_data.todo == 'add':
        if user.username is not None:
            frm = f'<a href="tg://user?id={user.id}">@{user.username}</a>'
        else:
            frm = f'<a href="tg://user?id={user.id}">@{user.first_name + user.last_name}</a>'
    else:
        frm = '@анонім'

    disabled_links = LinkPreviewOptions(is_disabled=True)
    if photo:
        txt = f"нова валентинка! ❤\nдля кого: {to}\nвід кого: {frm}"
        if text:
            txt += f"\n\n<tg-spoiler>{text}</tg-spoiler>"

        await bot.send_photo(settings.bots.val_main_id, photo, caption=txt)
        await bot.send_photo(settings.bots.val_logs_id, photo, caption=txt)

    else:
        text = f"нова валентинка! ❤\nдля кого: {to}\nвід кого: {frm}\n\n<tg-spoiler>{text}</tg-spoiler>"

        await bot.send_message(settings.bots.val_main_id, f'{text}', link_preview_options=disabled_links,
                               disable_web_page_preview=True)
        await bot.send_message(settings.bots.val_logs_id, f'{text}', link_preview_options=disabled_links,
                               disable_web_page_preview=True)

    name = str(user.first_name)+str(user.last_name)
    await request.add_valentine(user_id=user.id, username=user.username, name=name, to_user=to)
    await call.message.edit_text('зроблено! ❤')
    await state.clear()
    await call.answer()


async def valentine_get_cancel(message: Message, bot: Bot, request: Request, state: FSMContext):
    await state.clear()
    await message.answer('уходиш ну і уходь')




