from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Button1'
        ),
        KeyboardButton(
            text='Button2'
        ),
        KeyboardButton(
            text='Button3'
        )
    ],
    [
        KeyboardButton(
            text='Button4'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Choose", selective=True)

loc_tel_poll_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Send geo',
            request_location=True
        ),
    ],
    [
        KeyboardButton(
            text='Send phone',
            request_contact=True
        ),
    ],
    [
        KeyboardButton(
            text='Send quiz',
            request_poll=KeyboardButtonPollType()  # type = regular / quiz
        ),
    ]
], resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Create / Send", selective=True)


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Btn1")
    keyboard_builder.button(text="Btn2")
    keyboard_builder.button(text="Btn3")
    keyboard_builder.button(text="Send geo", request_location=True)

    keyboard_builder.adjust(1, 2, 1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder="Create / Send", selective=True)
