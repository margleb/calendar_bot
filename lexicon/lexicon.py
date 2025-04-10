
# dialogs/common/start.py
DC_START: dict[str, str | dict] = {
    'start': (
        "Привет, {username}! Я бот позволяющий организовывать мероприятия и находить их. "
        "Если хочешь <b>куда-то сходить</b>, то выбери <b>календарь событий</b>, "
        "а если хочешь <b>зайти в свой аккаунт</b>, то выбери <b>мой аккаунт</b>"
    ),
    'buttons': {
        'account': "👤 Мой аккаунт",
        'calendar': "📅 Календарь событий"
    }
}

DU_CALENDAR: dict[str, str] = {
    'calendar': 'Выберите дату когда вы хотите <b>организовать</b> либо <b>посетить мероприятие</b>:'
}

D_BUTTONS: dict[str, str] = {
    'back': '◀️ Назад'
}