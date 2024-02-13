from aiogram.filters.callback_data import CallbackData


class CallbackTestInfo(CallbackData, prefix='btn'):
    btn_num: int


class CallbackMainMenu(CallbackData, prefix='mm'):
    todo: str
    task_num: int


class CallbackStartVoting(CallbackData, prefix='vote-begin'):
    todo: int


class CallbackVoting(CallbackData, prefix='vote'):
    candidate: str


class CallbackConfirmVoting(CallbackData, prefix='confirm-vote'):
    todo: str


class CallbackAddAsAuthor(CallbackData, prefix='val-author'):
    todo: str
