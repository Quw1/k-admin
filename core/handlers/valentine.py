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

STICKER_1 = "CAACAgEAAxkBAAEpdfVly4OSYISFTCWfdsY13siwxFpnWAACgAEAAnY3dj-N4Xs2gVMb7DQE"
STICKER_2 = "CAACAgEAAxkBAAEpdfNly4MQpCyNTavaQcNaGsQ-KBDkEQACEQEAAnY3dj8PX08Hh0bD5jQE"
STICKER_3 = "CAACAgEAAxkBAAEpdfply4Sx36wJFeLzRwcN5_ZtrqmzDAAC2wEAAizw6Ebki74oV6hSZjQE"
STICKER_4 = "CAACAgEAAxkBAAEpdfxly4TklQ2kRMv3PhsGjKOk22VUngACsQEAAnY3dj-kdqoozr_pczQE"
STICKER_5 = "CAACAgEAAxkBAAEpdi5ly43xZE2Cm6XNKywdmMMWgigXIgACfgEAAnY3dj8UjQY54xnG7zQE"
disabled_links = LinkPreviewOptions(is_disabled=True)

async def valentine_start(message: Message, bot: Bot, request: Request, state: FSMContext):
    if message.chat.type != 'private':
        await message.reply('приймаю лише в приватних повідомленнях <3')
    else:
        await message.answer('ну давай, кого любимо на цей раз?\n\nнапиши у форматі <b>@username</b>\n\nякщо у людини'
                             ' нема @username, можеш написати її ім\'я так, щоб вона змогла знайти валентинку '
                             '(наприклад: Діма Остапенко К-24)\n\n<i>якщо захочеш зупинити процес, тикай <b>/lonely</b>'
                             ' (тю, навіть не спробуєш?)</i>')
        await state.set_state(Valentine.GET_TO)


async def valentine_get_to(message: Message, bot: Bot, request: Request, state: FSMContext):
    if not message.text:
        await message.answer_sticker(sticker=STICKER_1)
        await message.answer('чел ти... напиши текстом нік/ім\'я')
    else:
        if len(message.text) > 30:
            await message.answer_sticker(sticker=STICKER_1)
            await message.answer('пиши нормально - максимум 30 літер')
        elif len(message.text) < 5:
            await message.answer_sticker(sticker=STICKER_1)
            await message.answer('пиши нормально - мінімум 5 літер')
        else:
            to = message.text.replace("*", "\\*")\
                .replace("[", "\\[")\
                .replace("`", "\\`")
            to = html.escape(to, quote=True)

            if to.isascii() and ' ' not in to and '@' not in to:
                to = '@' + to

            await state.update_data(to=to)
            await state.set_state(Valentine.GET_MSG)
            await message.answer('а тепер шо ти хочеш людині сказати?\n\nнадсилай або текстове повідомлення, або кидай '
                                 'фотку/картинку\n\nнаприклад, звідси: <a href="https://t.me/kft_cj/711">шльоп</a>'
                                 '\nрекомендую на картинці вказати кому та від '
                                 'кого ще раз :)\n\n<i>P.S: якшо хочеш шось інше за текст або фотку, то напиши '
                                 'адмінам <b>@kft_cj_bot</b></i> 🤑',
                                 disable_web_page_preview=True,
                                 link_preview_options=disabled_links)


async def valentine_get_message(message: Message, bot: Bot, request: Request, state: FSMContext):
    if (not message.text) and (not message.photo):
        await message.answer_sticker(STICKER_4)
        await message.answer('дозволені лише фотки та текстові повідомлення\n\nале якшо дуже хочеш щось інше, можеш '
                             'домовитись з адмінами <b>@kft_cj_bot</b> 🤑')
    else:
        if message.text:
            if len(message.text) > 500:
                await message.answer_sticker(STICKER_5)
                await message.answer('книгу пишеш? не більше 500 символів у повідомленні')
                return
            else:
                msg = message.text.replace("*", "\\*") \
                    .replace("[", "\\[") \
                    .replace("`", "\\`")
                msg = html.escape(msg, quote=True)
                await state.update_data(text=msg)
        else:
            if message.caption is not None:
                msg = message.caption.replace("*", "\\*") \
                    .replace("[", "\\[") \
                    .replace("`", "\\`")
                msg = html.escape(msg, quote=True)
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
    name_from = str(user.first_name or '') + '' + str(user.last_name or '')
    if name_from != '':
        name_from = html.escape(name_from)

    if user.username is not None:
        frm = f'@{user.username}'
        admin_frm = f'@{user.username}'
    else:
        frm = f'<a href="tg://user?id={user.id}">@{name_from}</a>'
        admin_frm = f'<a href="tg://user?id={user.id}">@{name_from}</a>'

    if callback_data.todo != 'add':
        frm = '@анонім'


    if photo:
        txt = f"<b>ВАЛЕНТИНКА! </b>💌\n\n<i>для кого: </i>{to}\n<i>від кого: </i>{frm}"
        txt_admin = f"<b>ВАЛЕНТИНКА! </b>💌\n\n<i>для кого: </i>{to}\n<i>від кого: </i>{admin_frm}"
        if text:
            txt += f"\n\n<tg-spoiler>{text}</tg-spoiler>"
            txt_admin += f"\n\n{text}"

        await bot.send_photo(settings.bots.val_main_id, photo, caption=txt, has_spoiler=True)
        await bot.send_photo(settings.bots.val_logs_id, photo, caption=txt_admin)

    else:
        text_user = f"<b>ВАЛЕНТИНКА! </b>💌\n\n<i>для кого: </i>{to}\n<i>від кого: </i>{frm}\n\n<tg-spoiler>{text}</tg-spoiler>"
        text_admin = f"<b>ВАЛЕНТИНКА! </b>💌\n\n<i>для кого: </i>{to}\n<i>від кого: </i>{admin_frm}\n\n{text}"

        await bot.send_message(settings.bots.val_main_id, f'{text_user}', link_preview_options=disabled_links,
                               disable_web_page_preview=True)
        await bot.send_message(settings.bots.val_logs_id, f'{text_admin}', link_preview_options=disabled_links,
                               disable_web_page_preview=True)

    await request.add_valentine(user_id=user.id, username=user.username, name=name_from, to_user=to)
    await call.message.answer_sticker(STICKER_3)
    await call.message.edit_text('зроблено! ❤')
    await state.clear()
    await call.answer()


async def valentine_get_cancel(message: Message, bot: Bot, request: Request, state: FSMContext):
    await state.clear()
    await message.answer_sticker(STICKER_2)
    await message.answer('уходиш ну і уходь')


async def valentine_call_cancel(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackAddAsAuthor,
                             state: FSMContext):
    await call.answer()
    await call.message.edit_text('все фігня, давай по новій')



