# from aiogram import Bot
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, FSInputFile, InputMediaPhoto
# from core.keyboards.inline import get_main_menu_kb, get_main_menu_back_kb, task_menu
# from core.utils.dbconnect import Request
# from core.utils.statelogin import UserState
# from aiogram.types import CallbackQuery
# from core.utils.callbackdata import CallbackMainMenu
# from aiogram.utils.keyboard import InlineKeyboardBuilder
#
#
# async def show_menu(message: Message, bot: Bot, request: Request, state: FSMContext):
#     await bot.send_photo(message.from_user.id,
#                          'AgACAgIAAxkBAAIEBmSE37VRMu9jjfJcjq9EG6uDcRYcAAJIyDEbq9woSLnHJGEcdOc_AQADAgADeQADLwQ',
#                          reply_markup=get_main_menu_kb())
#
#
# async def show_info(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                     state: FSMContext):
#     await call.answer()
#     ph = InputMediaPhoto(media="AgACAgIAAxkBAAIDumSE05HEa2qYMwaoJf9N9mxv9rttAAIQyDEbq9woSIfo85hh4sd0AQADAgADeQADLwQ")
#     await call.message.edit_media(ph)
#     await call.message.edit_caption(caption='lorem ipsum dolor sit amet, '
#                                             'consectetur adiplorem ipsum dolor sit amet, consectetur adiplorem ipsum '
#                                             'dolor sit amet, consectetur adiplorem ipsum dolor sit amet, consectetur'
#                                             ' adip',
#                                     reply_markup=get_main_menu_back_kb())
#
#
# async def show_terms(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                      state: FSMContext):
#     await call.answer()
#     ph = InputMediaPhoto(media="AgACAgIAAxkBAAIDz2SE1AbjSUmlLdCV43Aa1jXYh7DQAAIVyDEbq9woSMroAZlRG1DaAQADAgADeQADLwQ")
#     await call.message.edit_media(ph)
#     await call.message.edit_caption(
#         caption='lorem ipsum dolor sit amet, consectetur '
#                 'adiplorem ipsum dolor sit amet, consectetur adiplorem ipsum dolor sit amet, '
#                 'consectetur adiplorem ipsum dolor sit amet, consectetur adip',
#         reply_markup=get_main_menu_back_kb())
#
#
# async def show_tasks(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                      state: FSMContext):
#     res = await request.get_tasks(call.from_user.id, 0)
#
#     tasks_kb = make_task_keyboard(res)
#     await state.update_data(task_type='tasks')
#     ph = InputMediaPhoto(media="AgACAgIAAxkBAAIDvWSE05XZnP6oBfegnjuQ8i9-rT_5AAIRyDEbq9woSLlkT42_I4gaAQADAgADeQADLwQ")
#     await call.message.edit_media(ph, reply_markup=tasks_kb)
#     # await call.message.edit_caption(caption='')
#     await call.answer()
#
#
# async def show_active_tasks(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                             state: FSMContext):
#     res = await request.get_tasks(call.from_user.id, 2)
#
#     tasks_kb = make_task_keyboard(res)
#     await state.update_data(task_type='tasks-active')
#     ph = InputMediaPhoto(media="AgACAgIAAxkBAAIDwGSE05mz4JAeFkADogoN_0fV89t3AAISyDEbq9woSH0Lae5OkMZKAQADAgADeQADLwQ")
#     await call.message.edit_media(ph, reply_markup=tasks_kb)
#     # await call.message.edit_caption(caption='')
#     await call.answer()
#
#
# async def show_done_tasks(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                           state: FSMContext):
#     res = await request.get_tasks(call.from_user.id, 1)
#
#     tasks_kb = make_task_keyboard(res)
#     await state.update_data(task_type='tasks-done')
#     ph = InputMediaPhoto(media="AgACAgIAAxkBAAIDw2SE05uDNZcuw9alZP6t8Evc4dEmAAITyDEbq9woSG7qgJWmD0MUAQADAgADeQADLwQ")
#     await call.message.edit_media(ph, reply_markup=tasks_kb)
#     # await call.message.edit_caption(caption='')
#     await call.answer()
#
#
# async def show_task(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                     state: FSMContext):
#     task_id = callback_data.task_num
#     context_data = await state.get_data()
#     task_type = context_data.get('task_type')
#     res = await request.get_task(task_id)
#
#     keyboard_builder = InlineKeyboardBuilder()
#     if res[4] == 0:
#         keyboard_builder.button(text='Взять задание', callback_data=CallbackMainMenu(todo='take-task',
#                                                                                      task_num=int(task_id)))
#     elif res[4] == 1:
#         keyboard_builder.button(text='Задание выполнено', callback_data=CallbackMainMenu(todo='alert-done',
#                                                                                          task_num=-1))
#     elif res[4] == 2:
#         keyboard_builder.button(text='Задание активно', callback_data=CallbackMainMenu(todo='alert-taken',
#                                                                                        task_num=-1))
#     else:
#         keyboard_builder.button(text='Задание недоступно', callback_data=CallbackMainMenu(todo='alert-unv',
#                                                                                           task_num=-1))
#
#     keyboard_builder.button(text='Назад', callback_data=CallbackMainMenu(todo=task_type, task_num=-1))
#     keyboard_builder.adjust(1)
#     task_kb = keyboard_builder.as_markup()
#     if res[4] == 0:
#         status = "Доступно 🈳"
#     elif res[4] == 1:
#         status = "Выполнено 💮"
#     elif res[4] == 2:
#         status = "Активно 🉑"
#     else:
#         status = "Недоступно 🈲"
#     text = f'<b>LOTUS 🪷 {res[1]}</b>\n\n<b>Описание: </b>{res[2]}\n\n<b>Награда: </b>{res[3]}\r\n' \
#            f'<b>Статус: </b>{status}'
#     await call.message.edit_caption(caption=text, reply_markup=task_kb)
#     await call.answer()
#
#
# async def back_to_main(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                        state: FSMContext):
#     ph = InputMediaPhoto(media="AgACAgIAAxkBAAIEBmSE37VRMu9jjfJcjq9EG6uDcRYcAAJIyDEbq9woSLnHJGEcdOc_AQADAgADeQADLwQ")
#     await call.message.edit_media(ph, reply_markup=get_main_menu_kb())
#     await call.answer()
#
#
# async def take_task(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                     state: FSMContext):
#     task_id = callback_data.task_num
#     await request.take_task(task_id)
#     keyboard_builder = InlineKeyboardBuilder()
#     keyboard_builder.button(text='◀ Назад', callback_data=CallbackMainMenu(todo='tasks', task_num=-1))
#     keyboard_builder.adjust(1)
#     task_kb = keyboard_builder.as_markup()
#     await call.message.edit_reply_markup(reply_markup=task_kb)
#
#
# async def alert_taken(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                       state: FSMContext):
#     await call.answer(text='🪷 Это задание уже активно.', show_alert=True)
#
#
# async def show_task_menu(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                          state: FSMContext):
#     ph = InputMediaPhoto(media="AgACAgIAAxkBAAIDxmSE050R32X-OA_kj_W_7Hsz6VZmAAIUyDEbq9woSO66UUvTHN1RAQADAgADeQADLwQ")
#     await call.message.edit_media(ph, reply_markup=task_menu())
#     # await call.message.edit_caption(caption='')
#     await call.answer()
#
#
# async def alert_done(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                      state: FSMContext):
#     await call.answer(text='🪷 Это задание уже выполнено.', show_alert=True)
#
#
# async def alert_unv(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackMainMenu,
#                     state: FSMContext):
#     await call.answer(text='🪷 Это задание недоступно.', show_alert=True)
#
#
# def make_task_keyboard(res):
#     keyboard_builder = InlineKeyboardBuilder()
#     for task in res:
#         keyboard_builder.button(text=task[1], callback_data=CallbackMainMenu(todo='task', task_num=int(task[0])))
#     keyboard_builder.button(text='◀ Назад', callback_data=CallbackMainMenu(todo='menu-tasks', task_num=-1))
#     keyboard_builder.adjust(1)
#     return keyboard_builder.as_markup()
