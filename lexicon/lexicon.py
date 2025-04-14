
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

DU_CALENDAR: dict[str, str | dict] = {
    'city': 'В каком городе ты живешь? Пока что бот работает для <b>Москвы</b> и <b>Cанкт-Петербурга</>:',
    'calendar': 'Выбери дату когда ты хочешь <b>организовать</b> либо <b>посетить мероприятие</b>:',
    'choice': 'Вот что ты можешь сделать на дату <b>{{date}}</b> в <b>{{city}}</>:\n{% if full_events %}Ты создал уже <b>больше 5 мероприятий</>! Дождись их окончания, либо удали несколько в <b>личном кабинете</b>{% endif %}',
    'result': '{{description}}\n\n────────────────────\n\n🎯 <b>Событие: </b>{{title}}\n\n🏙 <b>Локация: </b>{{city}}\n\n📆 <b>Дата проведения: </b>{{date}}\n\n💬 <b>Для связи: </b>@{{username}}',
    'buttons': {
        'create_event': "🎉 Создать мероприятие",
        'show_events': "📋 Посмотреть список мероприятий",
        'join_event': "✅ Я приду!",
        'cancel_event': "❌ Я НЕ пойду!",
        'next_event': ">>",
        'prev_event': "<<",
    }
}

DU_CREATE_EVENT: dict[str, str | dict] = {
    'title': 'Укажи название мероприятия, например: <b>Прогулка в парке</b> или <b>Сходить на шашлыки</b>.',
    'description': 'Добавь краткое описание мероприятию.',
    'result': "{{description}}\n\n────────────────────\n\n🎯 <b>Событие: </b>{{title}}\n\n🏙 <b>Локация: </b>{{city}}\n\n📆 <b>Дата проведения: </b>{{date}}\n\n💬 <b>Для связи: </b>@{{username}}",
    'moderation': "Ваше событие <b>{title}</b> отправлено на модерацию. Статус модерации вы можете посмотреть в <b>Личном кабинете</b>",
    'buttons': {
        'create_event': "Создать мероприятие",
        'apply_moderation': "Я понял!"
    }
}

HANDLERS: dict[str, str] = {
    'no_cmd': "Извини, я не знаю что такое <b>{message.text}</b>. Давайте лучше создадим мероприятие, нажми  <b>Создать мероприятие</b>",
    'support': "Если у вас есть какие-то идеи либо вопросы по работе бота, то напишите разработчику @margleb93"
}

D_BUTTONS: dict[str, str] = {
    'back': '◀️ Назад',
    'next': 'Вперед ▶️'
}