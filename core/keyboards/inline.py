from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import (CallbackTestInfo, CallbackMainMenu, CallbackVoting, CallbackConfirmVoting,
                                     CallbackStartVoting, CallbackAddAsAuthor)


inline_test = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Button 1",
            callback_data="btn-1"
        )
    ],
    [
        InlineKeyboardButton(
            text="Button 2",
            callback_data="btn-2"
        ),
        InlineKeyboardButton(
            text="Button 3",
            url="https://google.com"
        )
    ],
    [
        InlineKeyboardButton(
            text="Button 3",
            callback_data="btn-3"
        )
    ]
])


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Button 1', callback_data=CallbackTestInfo(btn_num=1))
    keyboard_builder.button(text='Button 2', callback_data=CallbackTestInfo(btn_num=2))
    keyboard_builder.button(text='Button 3', callback_data=CallbackTestInfo(btn_num=3))
    keyboard_builder.button(text='Profile', url='tg://user?id=5041922463')

    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()


def get_start_voting():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='почати', callback_data=CallbackStartVoting(todo=1))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_vote_markup():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Вікторія Кондратюк', callback_data=CallbackVoting(candidate='Вікторія Кондратюк'))
    keyboard_builder.button(text='Дмитро Остапенко', callback_data=CallbackVoting(candidate='Дмитро Остапенко'))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_confirm_vote_markup():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Так', callback_data=CallbackConfirmVoting(todo='confirmed'))
    keyboard_builder.button(text='Ні, хочу назад', callback_data=CallbackConfirmVoting(todo='back'))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_yes_no_markup():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='додати', callback_data=CallbackAddAsAuthor(todo='add'))
    keyboard_builder.button(text='анонімно', callback_data=CallbackAddAsAuthor(todo='no'))

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
