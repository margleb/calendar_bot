from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, EventContext, MediaId


async def get_event_data(dialog_manager: DialogManager, event_context: EventContext, **kwargs) -> dict:
    city = dialog_manager.start_data['selected_city']
    date_event = dialog_manager.start_data['selected_date']
    image_id = dialog_manager.dialog_data['photo']  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    username = event_context.chat.username  # получаем username
    return {
        'title': dialog_manager.find('title').get_value(),
        'description': dialog_manager.find('description').get_value(),
        'participants': dialog_manager.find('participants').get_value(),
        'photo': image,
        'city': city,
        'date': date_event,
        'username': username
    }